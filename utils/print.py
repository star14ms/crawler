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


def len_str(text):
    return sum(2 if east_asian_width(ch) in 'FW' else 1 for ch in str(text))


def rstrip_until_endline(text, len, max_len):
    if len > max_len:
        over_len = len - max_len
        idx = -1
        while len_str(text[idx:]) < over_len:
            idx -= 1
        text = text[:idx]
    
    return text


def add_spaces_until_endline(text: str = "", shortening_end='..', align_right_side: bool = False):
    text = RE_ANSI.sub('', text)
    max_len = 150 + 1 - len_str(shortening_end)
    
    text2 = rstrip_until_endline(text, len_str(text), max_len)
    if shortening_end and text!=text2: 
        text2 = text2 + shortening_end

    del_len = sum(1 if east_asian_width(ch) in 'FW' else 0 for ch in str(text2))

    return text2.ljust(max_len - del_len) if not align_right_side else text2.rjust(max_len - del_len)
