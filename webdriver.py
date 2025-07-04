from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time
from utils import Time


def get_chrome_driver(headless=True):
    """브라우저 원격 접속 인터페이스"""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.set_window_position(0, 0)
    driver.set_window_size(800, 800)

    return driver


def pause_video(driver):
    video = driver.find_element(By.TAG_NAME, 'video') # 'ytp-play-button'
    driver.execute_script("arguments[0].pause()", video)
    time.sleep(0.5)


def scroll_down(driver, n_scroll_down=500, start_time=None, finish_text="완료", waiting_time=0.1, selector_to_count=None):
    """스크롤 내리기 반복"""
    body = driver.find_element(By.TAG_NAME, 'body')

    for n in range(1, n_scroll_down+1):
        sys.stdout.write('\r스크롤 내리기 %d / %d' % (n, n_scroll_down) + \
            ('' if start_time is None else ' (%s)' % Time.str_delta(start_time))
        )
        sys.stdout.flush()

        body.send_keys(Keys.END)
        driver.implicitly_wait(10)
        time.sleep(waiting_time)

    sys.stdout.write('\r%s %d / %d' % (finish_text, n, n) + \
        ('' if start_time is None else ' (%s)' % Time.str_delta(start_time))
    )
    sys.stdout.flush()
