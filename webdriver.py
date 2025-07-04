from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time
from utils import Time
from utils.print import pad_spaces


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


def parse_selector(selector):
    if selector.startswith('.'):
        return (By.CLASS_NAME, selector[1:])
    elif selector.startswith('#'):
        return (By.ID, selector[1:])
    else:
        return (By.TAG_NAME, selector)


def scroll_down(driver, start_time=None, finish_text="완료", waiting_time=0.1, selector_to_count=None, max_elements=1000, no_change_timeout=2):
    """스크롤 내리기 반복 - 요소 개수 기반으로 중단"""
    body = driver.find_element(By.TAG_NAME, 'body')
    previous_count = 0
    last_change_time = time.time()
    n = 0

    # Initial scroll to trigger comment loading
    for _ in range(5):
        body.send_keys(Keys.END)
        driver.implicitly_wait(10)
    time.sleep(no_change_timeout)

    # Check if any elements exist after initial scroll
    if selector_to_count[1] not in driver.page_source:
        initial_count = 0
    else:
        initial_count = len(driver.find_elements(*selector_to_count))
    
    if initial_count == 0:
        sys.stdout.write(pad_spaces("\r%s 0 (요소: 0, 댓글 없음)" % finish_text + \
            ('' if start_time is None else ' (%s)' % Time.str_delta(start_time))))
        sys.stdout.flush()
        return
    
    while True:
        n += 1
        
        # Count current elements
        try:
            current_count = len(driver.find_elements(*selector_to_count))
        except:
            current_count = 0
        
        sys.stdout.write(pad_spaces("\r스크롤 내리기 %d (댓글 수: %d)" % (n, current_count) + \
            ('' if start_time is None else ' (%s)' % Time.str_delta(start_time))))
        sys.stdout.flush()
        
        # Check if count has changed
        if current_count != previous_count:
            last_change_time = time.time()
        
        # Stop conditions
        if max_elements and current_count >= max_elements or time.time() - last_change_time >= no_change_timeout:
            break

        previous_count = current_count
        
        # Scroll down
        body.send_keys(Keys.END)
        driver.implicitly_wait(10)
        time.sleep(waiting_time)
    
    # Final count
    try:
        final_count = len(driver.find_elements(*selector_to_count))
    except:
        final_count = 0
    
    sys.stdout.write(pad_spaces("\r%s %d (댓글 수: %d)" % (finish_text, n, final_count) + \
        ('' if start_time is None else ' (%s)' % Time.str_delta(start_time))))
    sys.stdout.flush()
