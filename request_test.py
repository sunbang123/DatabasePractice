import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}
data = requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers=headers)

print("status_code:", data.status_code)
print("응답 길이:", len(data.text))
print(data.text[:1000])  # 앞부분만 출력해서 실제로 뭐가 오는지 확인