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
