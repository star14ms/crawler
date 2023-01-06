from bs4 import BeautifulSoup
from rich import print as pprint
from rich.syntax import Syntax
from unicodedata import east_asian_width
import re


def print_html(soup):
    """HTML을 줄 번호, 들여쓰기 적용 등 예쁘게 출력"""

    if not isinstance(soup, BeautifulSoup):
        soup = BeautifulSoup(str(soup), "html.parser")

    syntax = Syntax(soup.prettify(), "html", theme="monokai", line_numbers=True, word_wrap=True)
    pprint(syntax)


RE_ANSI = re.compile(r"\x1b\[[;\d]*[A-Za-z]")


def width_str(text):
    return sum(2 if east_asian_width(ch) in 'FW' else 1 for ch in str(text))


def rstrip_until_max_width(text, max_w):
    real_w = width_str(text)
    if real_w > max_w:
        over_w = real_w - max_w
        while over_w > 0:
            over_w -= width_str(text[-1])
            text = text[:-1]
    
    return text


def pad_spaces(text: str = "", console_width: int = 150, ellipsis_text: str = '..', align_right_side: bool = False):
    text = RE_ANSI.sub('', text)
    max_width = console_width + 1 - width_str(ellipsis_text)

    text2 = rstrip_until_max_width(text, max_width)
    if ellipsis_text and text!=text2: 
        text2 = text2 + ellipsis_text

    del_len = sum(1 if east_asian_width(ch) in 'FW' else 0 for ch in str(text2))

    return text2.ljust(max_width - del_len) if not align_right_side else text2.rjust(max_width - del_len)
