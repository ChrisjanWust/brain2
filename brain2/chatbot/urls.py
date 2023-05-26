from django.urls import path

from brain2.chatbot.views import msg

app_name = "chatbot"
urlpatterns = [
    path("msg/", view=msg, name="msg"),
]
