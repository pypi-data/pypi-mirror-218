"""
    Semp-Progressbar
    v0.6.5
"""
from tqdm import trange,tqdm
from tqdm.gui import tqdm as guitqdm
from time import sleep
from requests import get
from sys import set_int_max_str_digits as max
from pathlib import Path
from random import randint


max(0)
class ChunkError:
    def __init__(self,*args,**kwargs):
        pass

def VirtualProgressbar(description:str = ...,time:int = 0.1):
    bar=tqdm(range(100))
    bar.set_description(description)
    for x in bar:
        sleep(time)

def EasyProgressbar():
    for __count in trange(100):
        sleep(0.1)

def DownloadProgressbar(description:str = "Downloading...",website: str = ...,name: str = ...,chunk_size=None):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}
    res = get(website, stream=True, headers=headers)
    length = float(res.headers['content-length'])
    f = open(name, 'wb')
    pbar = tqdm(total=length, initial=Path(name).stat().st_size, unit_scale=True, desc=description, ncols=120)
    if chunk_size == None:
        size=randint(256,5120)
        for chuck in res.iter_content(chunk_size=size):

            pbar.update(len(chuck))
            kb=size/1024
            pbar.set_postfix_str(f"{str(kb)}KB/s")
            f.write(chuck)
        f.close()
    else:
        try:
            temp=chunk_size+114514
        except:
            raise ChunkError("Not a integer value")
        else:
            for chuck in res.iter_content(chunk_size=chunk_size):
                f.write(chuck)
                pbar.update(len(chuck))
                kb = chunk_size / 1024
                pbar.set_postfix_str(f"{str(kb)}KB/s")
            f.close()
