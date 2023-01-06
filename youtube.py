import sys, os
import time, datetime

from .webdriver import pause_video, scroll_down, save_text_list
from .utils import pad_spaces


def crawl_youtube_comments(driver, urls, titles, comment_block, save_path=None, n_scroll_down=500, start_time=None, skip_video_until_n_comment=0):
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
            sys.stdout.write(pad_spaces("\r{0} | 완료 | {1}".format(i+1, titles[i])))
            sys.stdout.flush()
            continue

        # 웹 사이트 가져오기
        driver.get(url)
        driver.implicitly_wait(10)
        time.sleep(0.2)
        
        # 동영상 일시정지, 스크롤 내리기 반복
        pause_video(driver)
        scroll_down(driver, n_scroll_down, start_time, finish_text="댓글 수집 중...")

        # 댓글들 가져오기
        comment_blocks = driver.find_elements(*comment_block)
    
        if len(comment_blocks) < skip_video_until_n_comment:
            sys.stdout.write(pad_spaces("\r{0} | 스킵 | {1}".format(i+1, titles[i])))
            sys.stdout.flush()
            continue

        # txt파일로 댓글 저장
        comments = list(map(lambda cmt: cmt.text, comment_blocks))
        n_comment_saved = save_text_list(save_path, comments)

        # 댓글 수집한 동영상 목록에 현재 url추가
        with open(urls_save_path, 'a', encoding="utf-8") as f:
            f.write(url+'\t'+titles[i]+'\n')

        saved_cmts_num += n_comment_saved
    
        sys.stdout.write(pad_spaces("\r{0} | {1}개 | {2}".format(i+1, len(comments), titles[i])))
        sys.stdout.flush()
    
    print('\n수집한 댓글 수: %d개'% saved_cmts_num)
