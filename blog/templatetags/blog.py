"""Blog template tags."""

from typing import List
from django import template
from blog.models import Post


register = template.Library()


@register.inclusion_tag('blog/components/list.html')
def post_list(posts: List[Post]):
    return {'posts': posts}


@register.inclusion_tag('blog/components/list_item.html')
def post_list_item(post: Post):
    return {'post': post}
