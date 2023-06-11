from django.conf import settings

import openai

openai.api_key = settings.OPENAI_API_KEY


def chat_with_gpt(system_msg: str, user_msg: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            # {
            #     "role": "system",
            #     "content": system_msg,
            # },
            {
                "role": "user",
                "content": 'Yesterday: "' + system_msg + '"\n\nNow: "' + user_msg + '"',
            },
        ],
    )
    reply: str = response.choices[0].message.content
    reply = reply.replace(", as an AI language model,", ",", 1)
    return reply
