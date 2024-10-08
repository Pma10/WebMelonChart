import requests
import os
import base64
from datetime import datetime
from bs4 import BeautifulSoup

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
def upload_gitAction(data: str):
    try:
        token = os.environ.get('TOKEN')
        url = "https://api.github.com/repos/Pma10/WebMelonChart/issues"
        response = requests.post(url, json={"title": f"{datetime.now().strftime('%Y년 %m월 %d일')} 멜론차트 TOP100", "body": data}, headers={"Authorization": f"token {token}"})
        response.raise_for_status()
        print('업로드 성공')
    except requests.exceptions.RequestException as e:
        print('업로드 실패:', e)

def upload_to_github(file_path: str, repo: str, branch: str = 'main'):
    try:
        token = os.environ.get('TOKEN')
        username = "Pma10"
        commit_message = f"{datetime.now().strftime('%Y-%m-%d')} 멜론차트 업데이트"
        
        with open(file_path, 'rb') as file:
            content = base64.b64encode(file.read()).decode('utf-8')

        url = f'https://api.github.com/repos/{username}/{repo}/contents/{file_path}'
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
        }
        data = {
            'message': commit_message,
            'content': content,
            'branch': branch,
        }
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        print('업로드 성공')
    except requests.exceptions.RequestException as e:
        print('업로드 실패:', e)

def get_melon_chart():
    try:
        melon100 = requests.get("https://www.melon.com/chart/index.htm", headers=header).text
        soup = BeautifulSoup(melon100, 'html.parser')
        titles = soup.select('div.ellipsis.rank01 > span')
        authors = soup.select('div.ellipsis.rank02 > span')
        return [title.text for title in titles], [author.text for author in authors]
    except requests.exceptions.RequestException as e:
        print('멜론 차트 데이터를 가져오는 데 실패했습니다:', e)
        return [], []

charts = []
charts_web = []

titles, authors = get_melon_chart()
for rank in range(len(titles)):
    title_name = titles[rank].replace('\n', '').strip()
    charts.append(f"TOP {rank + 1} {title_name} / {authors[rank]}\n")
    charts_web.append(f"TOP {rank + 1} {title_name} / {authors[rank]}<br>")

file_path = f'static/melon/{datetime.now().strftime("%Y-%m-%d")}.melon'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write("".join(charts_web))

upload_to_github(file_path, 'WebMelonChart', 'main')

upload_gitAction("".join(charts)) 
