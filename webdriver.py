from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time
from utils.common import Time


def get_chrome_driver(executable_path='chromedriver'):
    """브라우저 원격 접속 인터페이스"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=executable_path, options=options)
    driver.set_window_position(0, 0)
    driver.set_window_size(800, 800)

    return driver


def pause_video(driver):
    video = driver.find_element('tag name', 'video') # 'ytp-play-button'
    driver.execute_script("arguments[0].pause()", video)
    webdriver.ActionChains(driver).click(video).perform() # webdriver.ActionChains(driver).send_keys(Keys.SPACE)
    time.sleep(0.5)


def scroll_down(driver, n_scroll_down=500, waiting_time=0.1, start_time=None, finish_text="완료"):
    """스크롤 내리기 반복"""
    body = driver.find_element('tag name', 'body')

    for n in range(1, n_scroll_down+1):
        sys.stdout.write('\r스크롤 내리기 %d / %d' % (n, n_scroll_down) + \
            '' if start_time is None else ' (%s)' % Time.str_delta(start_time)
        )
        sys.stdout.flush()

        body.send_keys(Keys.END)
        driver.implicitly_wait(10)
        time.sleep(waiting_time)

    sys.stdout.write('\r%s %d / %d' % (finish_text, n, n) + \
        '' if start_time is None else ' (%s)' % Time.str_delta(start_time)
    )
    sys.stdout.flush()


def save_text_list(file_name, text_list):
    skip_num = 0

    with open(f'{file_name}.txt', 'a', encoding="utf-8") as f: 
        for text in text_list:
            text = text.replace('\n', ' ')
            if len(text)==0: 
                skip_num += 1
            else:
                f.write(text + '\n')

    n_comment_saved = len(text_list) - skip_num

    return n_comment_saved
