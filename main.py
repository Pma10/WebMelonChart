import requests
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re

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

def generate_date_options():
    current_date = datetime.now()
    dates = [(current_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    return dates

def update_html_date_options(html_file_path):
    date_options = generate_date_options()
    
    with open(html_file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        
        match = re.search(r'let dateOptions = \[([^\]]*)\];', content)
        if match:
            current_options = match.group(1).strip()
            if current_options:
                current_options = set(current_options.split(', '))
            else:
                current_options = set()
            
            new_dates = set(date_options)
            updated_dates = sorted(current_options.union(new_dates))

            new_date_options = ', '.join(f'"{date}"' for date in updated_dates)
            updated_content = re.sub(r'let dateOptions = \[([^\]]*)\];', f'let dateOptions = [{new_date_options}];', content)
            
            file.seek(0)
            file.write(updated_content)
            file.truncate()

charts = []
charts_web = []

titles, authors = get_melon_chart()
for rank in range(len(titles)):
    title_name = titles[rank].replace('\n', '').strip()
    charts.append(f"TOP {rank + 1} {title_name} / {authors[rank]}\n")
    charts_web.append(f"TOP {rank + 1} {title_name} / {authors[rank]}<br>")

with open(f'static/melon/{datetime.now().strftime("%Y-%m-%d")}.pm', 'w', encoding='utf-8') as f:
    f.write("".join(charts_web))

upload_gitAction("".join(charts))

update_html_date_options("src/routes/+page.svelte")
