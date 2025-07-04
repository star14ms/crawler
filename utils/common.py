from urllib.request import urlopen
import time


def save_text_list(file_path, text_list):
    with open(file_path, 'a', encoding="utf-8") as f: 
        for text in text_list:
            text = text.replace('\n', ' ')
            f.write(text + '\n')
    return len(text_list)


def save_image(img_url: str, file_path: str):
    with open(file_path, 'wb') as f: # w: write, b: binary
        byte = urlopen(img_url).read()
        f.write(byte)


class Time:
    def now():
        return time.perf_counter()

    def sec_to_hms(second):
            second = int(second)
            h, m, s = (second // 3600), (second//60 - second//3600*60), (second % 60)
            return h, m, s
    
    def str_delta(start_time, hms=False, rjust=False, join=':'):
        time_delta = time.perf_counter() - start_time
        h, m, s = Time.sec_to_hms(time_delta)
        if not hms:
            return "{1}{0}{2:02d}{0}{3:02d}".format(join, h, m, s)
        elif rjust: 
            m, s = str(m).rjust(2), str(s).rjust(2)
        
        return str(f"{h}h{join}{m}m{join}{s}s")
