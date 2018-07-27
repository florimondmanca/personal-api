"""Banners views."""

from io import BytesIO

from django.http import HttpResponse

from .utils import Banner


def download_banner(request, text: str, filename) -> HttpResponse:
    """Generate and download a post banner."""
    image = Banner().generate(text)

    stream = BytesIO()
    image.save(stream, format='png')
    stream.seek(0)

    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    response.write(stream.read())

    return response
