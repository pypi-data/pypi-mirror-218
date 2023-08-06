from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from .template import *
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
from typing import Optional
import datetime
import re
import ctypes
import base64
import io

__all__ = ['Template']


FONT_PATH = 'C:\Windows\Fonts\Microsoft YaHei UI'
YAHEI_NORMAL = str(Path(FONT_PATH, 'msyh.ttc'))
YAHEI_THIN = str(Path(FONT_PATH, 'msyhl.ttc'))
SONGTI = str(Path(FONT_PATH, 'simsun.ttc'))

class ScreenResolutionNotSupportError(Exception):
    def __init__(self, msg):
        self.msg = msg

def splice(
    save_path: str,
    title_text: str,
    url_text: str,
    base_pic_path: Optional[str] = None,
    base_pic_as_base64: Optional[bytes] = None,
    template: Optional[Template] = None,
):
    if base_pic_path:
        base_image = Image.open(base_pic_path)
    elif base_pic_as_base64:
        image_data = base64.b64decode(base_pic_as_base64)
        base_image = Image.open(io.BytesIO(image_data))
    else:
        raise ValueError("Either 'base_pic_path' or 'base_pic_as_base64' must be provided.")
    
    nav_image = Image.open(template.nav_pic_path)
    footer_image = Image.open(template.footer_pic_path)

    # 时间拼接
    time_pic = _time_generater(
        template.time_format, 
        template.date_format, 
        template.time_size, 
        template.time_background_color,
        template.time_font_color,
    )
    footer_image.paste(time_pic, template.time_draw_position)

    # 标题拼接
    title_pic = _title_generater(title_text, template.title_size)
    nav_image.paste(title_pic, template.title_draw_position)

    # 网址栏拼接
    url_pic = _url_generater(url_text, template.url_size)
    nav_image.paste(url_pic, template.url_draw_position)

    # 获取基础图片的尺寸
    base_width, base_height = base_image.size
    # 获取导航栏图片的尺寸
    nav_width, nav_height = nav_image.size
    # 获取底边栏图片的尺寸
    footer_width, footer_height = footer_image.size

    # 调整长宽一致
    nav_scale = base_width / nav_width
    footer_scale = base_width / footer_width
    nav_new_height = int(nav_height * nav_scale)
    footer_new_height = int(footer_height * footer_scale)
    nav_image = nav_image.resize((base_width, nav_new_height))
    footer_image = footer_image.resize((base_width, footer_new_height))

    # 创建一个新的图片
    new_image = Image.new('RGB', (base_width, base_height+nav_new_height+footer_new_height))
    new_image.paste(nav_image, (0, 0))
    new_image.paste(base_image, (0, nav_new_height))
    new_image.paste(footer_image, (0, base_height+nav_new_height))

    new_image.save(save_path)

def _time_generater(time_format, date_format, size, background_color, font_color):
    image = Image.new('RGB', size, background_color)
    font = ImageFont.truetype(YAHEI_NORMAL, 12)
    
    #获取当前时间
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.strftime(time_format)
    current_date = current_datetime.strftime(date_format)
    
    # 在图像上绘制文本
    draw = ImageDraw.Draw(image)
    draw.text(xy=(23, 1.5), text=current_time, fill=font_color, font=font)
    draw.text(xy=(7, 20), text=current_date, fill=font_color, font=font)

    return image

def _title_generater(text, size):
    background_color = (255, 255, 255)
    image = Image.new('RGB', size, background_color)
    font = ImageFont.truetype(YAHEI_THIN, 12)

    # 在图像上绘制文本3 
    draw = ImageDraw.Draw(image)
    draw.text(xy=(2, 3), text=text, fill=(0, 0, 0), font=font)

    return image

def _url_generater(text, size):
    background_color = (241, 243, 244)
    image = Image.new('RGB', size, background_color)
    font = ImageFont.truetype(YAHEI_NORMAL, 12)

    # 在图像上绘制文本
    draw = ImageDraw.Draw(image)
    result = re.search(r'(?!:\/\/)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}', text)
    base_width, base_height = (1, 2)
    
    if result:
        domain = result.group()
        proto, param = text.split(domain)

        draw.text(xy=(base_width, base_height), text=proto, fill=(105, 106, 108), font=font)

        width = font.getlength(proto)
        new_width = base_width + width
        draw.text(xy=(new_width, base_height), text=domain, fill=(0, 0, 0), font=font)

        width = font.getlength(proto+domain)
        new_width = base_width + width
        draw.text(xy=(new_width, base_height), text=param, fill=(105, 106, 108), font=font)
    else:
        draw.text(xy=(base_width, base_height), text=text, fill=(105, 106, 108), font=font)

    return image

def _get_user_screen_resolution():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def super_screenshot(driver: WebDriver, save_path: str, template: Optional[Template] = None) -> None:
    screen_resolution = _get_user_screen_resolution()

    if not template:
        if screen_resolution == (2560, 1440):
            template = DEFAULT_TEMPLATE_2
        else:
            template = DEFAULT_TEMPLATE_1
    else:
        if type(template) != Template:
            raise TypeError('The paramater "template" must be a Template object.')
        
    png = driver.get_screenshot_as_base64()
    url_text = driver.current_url

    try:
        title_text = driver.title
    except NoSuchElementException:
        title_text = url_text

    splice(save_path, title_text, url_text, base_pic_as_base64=png, template=template)