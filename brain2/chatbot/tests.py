from django.test import TestCase

from brain2.chatbot.logic import ResponseFormulator
from brain2.chatbot.models import Keyword
import pytest


def build_message_body(query) -> dict:
    return {
        "session": "projects/brain2-orpu/agent/sessions/40e8e41f-556d-36f3-b638-1f548171f520",
        "responseId": "0e22dbac-8342-47ba-aea1-6b5641efc22c-4c6e80df",
        "queryResult": {
            "intent": {
                "name": "projects/brain2-orpu/agent/intents/5ad458db-3943-4934-85c4-b0ed9cc6936c",
                "isFallback": True,
                "displayName": "CatchAll4Real",
            },
            "queryText": query,
            "parameters": {},
            "languageCode": "en",
            "outputContexts": [
                {
                    "name": "projects/brain2-orpu/agent/sessions/40e8e41f-556d-36f3-b638-1f548171f520/contexts/__system_counters__",
                    "parameters": {"no-input": 0.0, "no-match": 3.0},
                    "lifespanCount": 1,
                }
            ],
            "allRequiredParamsPresent": True,
            "intentDetectionConfidence": 1.0,
        },
        "originalDetectIntentRequest": {
            "source": "telegram",
            "payload": {
                "data": {
                    "chat": {"id": "59712280789", "type": "private"},
                    "date": "1685749027",
                    "from": {"id": "59712280789", "first_name": "Anakin", "language_code": "en"},
                    "text": "What colour is my jacket?",
                    "message_id": "63",
                }
            },
        },
    }


@pytest.mark.django_db
def test_account_id_generation():
    # todo: patch chatGpt responses
    nr_keywords = Keyword.objects.count()
    body = build_message_body("My jacket is yellow.")
    responder = ResponseFormulator(body)
    reply = responder.reply()
    assert Keyword.objects.count() - nr_keywords > 1

    body = build_message_body("What colour is my jacket?")
    responder = ResponseFormulator(body)
    reply = responder.reply()
    assert "yellow" in reply.lower()
