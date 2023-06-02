from dataclasses import dataclass
from nltk.stem import PorterStemmer

from .models import Context, Session, Account, Keyword
from .gpt import chat_with_gpt
from .words import random_okay_sentence, is_question, is_top_english_word


stemmer = PorterStemmer()


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
        self.keywords = self.extract_keywords(self.query)

    def reply(self):
        if not is_question(self.query):
            self.store_context()
            return random_okay_sentence()
        else:
            return chat_with_gpt(self.get_context(), self.query)

    def store_context(self):
        context = Context.objects.create(account_id=self.account_id, text=self.query)
        found_keyword_objects = list(Keyword.objects.filter(word__in=self.keywords))
        found_keywords_words = [keyword.word for keyword in found_keyword_objects]
        missing_keywords_words = [word for word in self.keywords if word not in found_keywords_words]
        missing_keyword_objects = Keyword.objects.bulk_create([Keyword(word=word) for word in missing_keywords_words])
        context.keywords.add(*(found_keyword_objects + missing_keyword_objects))

    def get_context(self) -> str:
        contexts = Context.objects.filter(
            account_id=self.account_id,
            keywords__word__in=self.keywords,
        ).order_by("created")
        return "Previous conversations:\n" + "\n".join([self.format_context(context) for context in contexts])

    @staticmethod
    def format_context(context: Context):
        return f'{context.created.weekday()}, {context.created.date()} {context.created.hour}h{context.created.minute}: "{context.text}"'

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

    @staticmethod
    def extract_keywords(sentence: str) -> list[str]:
        sentence = sentence.lower()
        for word in sentence.split(" "):
            if not is_top_english_word(word):
                yield stemmer.stem(word)
