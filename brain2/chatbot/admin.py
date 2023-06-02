from django.contrib import admin
from .models import Account, Session, Context, Keyword, Question


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "created")
    readonly_fields = ("id", "created")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "created")
    readonly_fields = ("id", "created")


@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "text", "created")
    readonly_fields = ("id", "created")


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("word",)
    filter_horizontal = ("contexts",)


@admin.register(Question)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("query",)
