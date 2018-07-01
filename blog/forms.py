"""Blog forms."""

from django import forms

from .models import Post


class PostCreateForm(forms.ModelForm):
    """Form for creating blog posts."""

    class Meta:  # noqa
        model = Post
        fields = ('title', 'content')
