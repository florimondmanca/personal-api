from django.contrib import admin, messages
from .models import APIKey


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    """Admin panel for API keys."""

    list_display = ('client_id', 'created', 'id')

    fieldsets = (
        (None, {'fields': ('client_id', 'key_message')}),
    )
    readonly_fields = ('key_message',)

    search_fields = ('id', 'client_id',)

    def key_message(self, obj):
        """Message displayed instead of the API key."""
        if obj.key:
            return '***************'
        return 'The API key will be generated once you click save.'
    key_message.short_description = 'Key'

    def save_model(self, request, obj, form, change):
        """Display the API key on save."""
        if not obj.pk:
            obj.save()
            messages.add_message(request, messages.WARNING, (
                f'The API key for {obj.client_id} is {obj.key}. '
                'Please note it down: you will not be able to see it again.'
            ))
        else:
            obj.save()
