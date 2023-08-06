from attr import define
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

@define
class Template:
    url_size: tuple

    time_background_color: tuple

    time_font_color: tuple

    nav_pic_path: Path

    footer_pic_path: Path

    time_draw_position: tuple

    title_draw_position: tuple = (42, 6)

    url_draw_position: tuple = (141, 42)

    title_size: tuple = (175, 23)

    time_size: tuple = (77, 39)

    time_format: str = "%H:%M"

    date_format: str = "%Y/%m/%d"

DEFAULT_TEMPLATE_1 = Template(
    time_background_color = (220, 221, 222),
    time_font_color = (0, 0, 0),
    url_size = (1530, 20),
    time_draw_position = (1745, 1),
    nav_pic_path = Path(BASE_DIR, 'ui', 'nav_1.png'),
    footer_pic_path = Path(BASE_DIR, 'ui', 'footer_1.png'),
)

DEFAULT_TEMPLATE_2 = Template(
    time_background_color = (78, 65, 68),
    time_font_color = (255, 255, 255),
    url_size = (2238, 20),
    time_draw_position = (2430, 1),
    nav_pic_path = Path(BASE_DIR, 'ui', 'nav_0.png'),
    footer_pic_path = Path(BASE_DIR, 'ui', 'footer_0.png'),
)