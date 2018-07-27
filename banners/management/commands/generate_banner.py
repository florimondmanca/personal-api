"""Management command to generate banners for blog posts."""
from django.core.management.base import BaseCommand, CommandError

from banners.utils import Banner
from blog.models import Post


class Command(BaseCommand):
    help = 'Generate a banner for a blog post'

    def add_arguments(self, parser):
        parser.add_argument(
            'slug',
            help='Slug of the post'
        )
        parser.add_argument(
            '-o',
            dest='output',
            help='Output file name',
        )
        parser.add_argument(
            '-i',
            dest='interactive',
            action='store_true',
            help='Interactive mode',
        )

    def handle(self, **options: dict):
        slug = options['slug']
        output = options['output'] or 'banner.png'
        interactive = options['interactive']
        try:
            post = Post.objects.get(slug__startswith=slug)
        except Post.DoesNotExist:
            raise CommandError(f'Post {slug} does not exist')

        if interactive:
            title = input(f'Enter title ({post.title}): ') or post.title
        else:
            title = post.title

        image = Banner().generate(title)
        image.save(output)

        self.stdout.write(self.style.SUCCESS(f'Banner generated at {output}.'))
