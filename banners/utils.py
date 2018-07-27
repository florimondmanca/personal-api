"""Post banner generation."""

import os
from PIL import Image, ImageDraw, ImageFont
from django.utils.text import wrap


DIR = os.path.dirname(__file__)


class Banner:
    """Generate banner images."""

    FONT_SIZE = 36
    FONT_NAME_REGULAR = 'regular.ttf'
    WRAP_WIDTH = 24
    LINE_SPACING = 0.4 * FONT_SIZE
    TEXT_COLOR = '#424242'
    BACKGROUND_COLOR = (255, 255, 255)
    DECORATION_COLOR = '#59c7b7'
    WIDTH = 480
    HEIGHT = 220

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = self._get_font(self.FONT_NAME_REGULAR)

    def generate(self, title: str) -> ImageDraw.Draw:
        image = Image.new(
            'RGB',
            (self.WIDTH, self.HEIGHT),
            self.BACKGROUND_COLOR
        )
        draw = ImageDraw.Draw(image)

        def size(text: str):
            return draw.multiline_textsize(
                text, font=self.font, spacing=self.LINE_SPACING)

        text = self.wrap(title)
        w, h = size(text)
        left = max(0, (self.WIDTH - w) / 2)
        y = max(0, (self.HEIGHT - h) / 2)

        self.write(draw, text, left, y)
        y += h + 1.2 * self.LINE_SPACING

        draw.line(
            [(left, y), (self.WIDTH / 2 + w / 2, y)],
            fill=self.DECORATION_COLOR,
            width=2,
        )

        return image

    def write(self, draw, text, x, y):
        draw.multiline_text(
            (x, y),
            text,
            fill=self.TEXT_COLOR,
            font=self.font,
            spacing=self.LINE_SPACING,
        )

    def wrap(self, text: str) -> str:
        return wrap(text, width=self.WRAP_WIDTH)

    def _get_font(self, name: str) -> ImageFont:
        font_path = os.path.join(DIR, 'assets', name)
        font = ImageFont.truetype(font_path, self.FONT_SIZE)
        return font
