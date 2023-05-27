from dataclasses import dataclass
from django.db.models import Q

from .models import Context, Session, Account
from .gpt import chat_with_gpt


@dataclass
class ResponseFormulator:
    body: dict

    def __post_init__(self):
        # set session and account (and create if not exists)
        self.session_id: str = self.body["session"].rsplit("/", 1)[-1]
        try:
            self.account_id = self.gen_account_id()
            Account.objects.get_or_create(id=self.account_id)
            Session.objects.get_or_create(id=self.session_id, account_id=self.account_id)
        except ValueError:
            self.account_id: str = Session.objects.get(id=self.session_id).account_id
        # query
        try:
            self.query: str = self.body["queryResult"]["queryText"]
        except KeyError:
            self.query = ""
        self.query = self.query.strip()

    def reply(self):
        if not self.is_question():
            Context.objects.create(account_id=self.account_id, text=self.query)
            return "Affirmative."
        else:
            return chat_with_gpt(self.get_context(), self.query)

    def is_question(self):
        # todo: at some point this needs to become much more advanced
        return self.query.endswith("?")

    def get_context(self) -> str:
        keywords = self.query.split()
        q = Q()
        for word in keywords:
            q |= Q(text__icontains=word)

        contexts = Context.objects.filter(account_id=self.account_id).filter(q)
        return "\n".join(contexts.values_list("text", flat=True))

    def gen_account_id(self):
        original_intent = self.body["originalDetectIntentRequest"]

        if not original_intent:
            raise ValueError("No account specified - 'originalDetectIntentRequest' key is empty.")

        channel = list(original_intent.keys())[0]
        identifier = self.extract_channel_id(channel, original_intent["payload"])
        return f"{channel}:{identifier}"

    @staticmethod
    def extract_channel_id(channel: str, payload: dict):
        if channel == "telegram":
            return payload["data"]["chat"]["id"]
