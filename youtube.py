import sys
import os
import time, datetime

from .webdriver import pause_video, scroll_down, parse_selector
from .utils import pad_spaces, save_text_list


def get_video_titles_URLs(driver, selector_video_block, URL):
    """URL에 접속하면 있는 모든 동영상의 제목과 링크 가져오기"""
    
    # 웹 사이트 가져오기
    driver.get(URL)
    driver.implicitly_wait(10)

    # 동영상 제목과 URL 모두 가져오기
    videos = driver.find_elements(*parse_selector(selector_video_block))

    titles, URLs = [], []
    for video in videos:
        href = video.get_attribute("href")
        if href is None or 'shorts' in href: continue
        
        # Clean URL by removing & parameters
        if '&' in href:
            href = href.split('&')[0]
            
        title = video.get_attribute("title")
        URLs.append(href)
        titles.append(title)

    print('\n찾은 동영상 갯수: %d개'% len(URLs))
    return URLs, titles


def crawl_youtube_comments(driver, urls, titles, selector_comment, save_path=None, max_comments_per_video=500, start_time=None, skip_video_until_n_comment=0):
    """링크에 하나씩 들어가 유튜브 댓글 크롤링하기"""

    print("0 | 댓글 수 | 동영상 제목")

    # 저장할 데이터 파일 이름 설정 (댓글, 동영상 링크 저장)
    if save_path is None:
        os.makedirs('./data/', exist_ok=True)
        day = datetime.date.today().strftime('%y%m%d')
        save_path = f'data/YT_cmts_{day}.txt'
    urls_save_path = save_path[:save_path.rfind('.')] + '_urls.txt'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # urls 파일이 존재하면 그 안의 url들은 제외하고 댓글 수집
    cmts_already_saved_urls = None
    if os.path.isfile(urls_save_path):
        with open(urls_save_path, 'r', encoding="utf-8") as f:
            cmts_already_saved_urls = [url_info.split('\t')[0] for url_info in f.read().splitlines()]
    
    saved_cmts_num = 0
    for i, url in enumerate(urls):
        
        # 댓글 수집한 동영상 목록에 있던 url이면 건너뛰기
        if cmts_already_saved_urls!=None and url in cmts_already_saved_urls:
            sys.stdout.write(pad_spaces("\r{0} | 완료 | {1}".format(i+1, titles[i]))+'\n')
            sys.stdout.flush()
            continue

        # 웹 사이트 가져오기
        driver.get(url)
        driver.implicitly_wait(10)
        time.sleep(0.2)
        
        # 동영상 일시정지, 스크롤 내리기 반복
        pause_video(driver)
        scroll_down(driver, start_time, finish_text="댓글 수집 중...", 
                   selector_to_count=parse_selector(selector_comment), max_elements=max_comments_per_video)

        # 댓글들 가져오기
        if parse_selector(selector_comment)[1] not in driver.page_source:
            comment_blocks = [] # 시간 단축을 위해 댓글이 없는 경우 바로 빈 리스트 반환
        else:
            comment_blocks = driver.find_elements(*parse_selector(selector_comment))
        
        if len(comment_blocks) < skip_video_until_n_comment:
            sys.stdout.write(pad_spaces("\r{0} | 스킵 | {1}".format(i+1, titles[i]))+'\n')
            sys.stdout.flush()
            continue

        comments = list(map(lambda cmt: cmt.text, comment_blocks))
        comments = [c for c in comments if c.replace('\n', ' ').strip()] # 빈 댓글 제거
        if len(comments) > max_comments_per_video:
            comments = comments[:max_comments_per_video]

        n_comment_saved = save_text_list(save_path, comments)

        # 댓글 수집한 동영상 목록에 현재 url추가
        with open(urls_save_path, 'a', encoding="utf-8") as f:
            f.write(url+'\t'+titles[i]+'\n')

        saved_cmts_num += n_comment_saved
    
        sys.stdout.write(pad_spaces("\r{0} | {1}개 | {2}".format(i+1, len(comments), titles[i]))+'\n')
        sys.stdout.flush()
    
    print('\n수집한 댓글 수: %d개'% saved_cmts_num)
