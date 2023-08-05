from typing import Union, List, Dict
import httpx
import re


def search(query: str, lang: str = "en", num: int = 10, headers: Union[Dict[str, str], None] = {"User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}) -> List[Union[dict, str]]:

    results: List[Union[dict, str]] = []

    headers["Accept-Charset"] = "utf-8"

    base_url: str = f"https://www.google.com/search?q={query}&num=30&hl={lang}"

    page: str = httpx.get(base_url, headers=headers).text

    web: str = '<div class="yuRUbf"><a href="(.*?)" data-jsarwt=".*?" ' \
               'data-usg=".*?" data-ved=".*?"><br><h3 class="LC20lb MBeuO DKV0Md">(.*?)</h3>.*?' \
               '<div class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf" style="-webkit-line-clamp:2">' \
               '<span>(.*?)</span></div>'

    for i in re.findall(pattern=web, string=page):
        url = i[0].split('" ')[0]
        results.append({
            "url": url,
            "title": i[1].replace('<span dir=\"ltr\">', "").replace("</span>", ""),
            "description": re.sub('<[^<>]+>', '', i[2])
        })

    return results[:num if len(results) > num else len(results)]
