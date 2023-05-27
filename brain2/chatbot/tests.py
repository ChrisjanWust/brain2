from django.test import TestCase

# Create your tests here.


def test_account_id_generation():
    body = {
        "originalDetectIntentRequest": {
            "source": "telegram",
            "payload": {
                "data": {
                    "chat": {"id": "5972280789", "type": "private"},
                    "from": {"first_name": "Chrisjan", "id": "5972280789", "language_code": "en"},
                    "entities": [{"length": 6.0, "type": "bot_command"}],
                    "message_id": "3",
                    "text": "/start",
                    "date": "1685137808",
                }
            },
        }
    }
