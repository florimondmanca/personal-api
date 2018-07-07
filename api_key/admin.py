from django.contrib import admin, messages
from .models import APIKey
from .utils import generate_key


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
        print(obj)
        if obj.key:
            return 'Hidden'
        return 'The API key will be generated once you click save.'

    def save_model(self, request, obj, form, change):
        """Display the API key on save."""
        if not obj.key:
            obj.key = generate_key()
            messages.add_message(request, messages.WARNING, (
                f'The API key for {obj.client_id} is {obj.key}. '
                'Please note it since you will not be able to see it again.'
            ))
        obj.save()
