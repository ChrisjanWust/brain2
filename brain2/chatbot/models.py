from django.db import models


class ModelBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Account(ModelBase):
    id = models.CharField(max_length=64, primary_key=True)


class Session(ModelBase):
    id = models.CharField(max_length=64, primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Context(ModelBase):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField()


class Keyword(models.Model):
    word = models.CharField(max_length=16)
    contexts = models.ManyToManyField(Context, related_name="keywords")


class Question(ModelBase):
    body = models.JSONField()
    query = models.CharField(max_length=200)
    generated_context = models.TextField()
