from django.contrib import admin
from .models import OAuthCredential, ChatMessage

admin.site.register(OAuthCredential)
admin.site.register(ChatMessage)
