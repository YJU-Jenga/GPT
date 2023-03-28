from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import pymysql
import config


def get_book_titles():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 브라우저가 뜨지 않고 실행됩니다.
    # chrome_options.add_argument("--disable-gpu")  # 하드웨어 가속 안함
    # chrome_options.add_argument("--lang=ko_KR")  # 사용언어 한국어
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 브라우저에서 이미지 로딩을 하지 않습니다.
    chrome_options.add_argument('--mute-audio')  # 브라우저에 음소거 옵션을 적용합니다.

    # 페이지네이션 갯수
    maximum = 20

    # title list
    title_list = []

    # 전래동화 크롤링
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options) as driver:
        for i in range(1, maximum + 1):
            URL = f"http://18children.president.pa.go.kr/our_space/fairy_tales.php?srh%5Bcategory%5D=07&srh%5Bpage%5D={i}"
            driver.get(URL)

            # 페이지 로딩 대기 (로딩이 완료되면 즉시 다음 코드 실행)
            driver.implicitly_wait(10)

            elements = driver.find_elements(By.CLASS_NAME, "title")

            for element in elements:
                title_name = element.find_elements(By.TAG_NAME, "a")
                title = title_name[0].text
                title_list.append(title)

    # 한글만 남게 하기
    title_replace = [re.sub(r"[^가-힣]", "", title) for title in title_list]
    return title_replace


# Database
db = pymysql.Connect(
    host='localhost',
    user='jenga',
    password=config.database_password,
    database='jenga',
    charset='utf8',
)
cursor = db.cursor()

# Database Table 초기화 하기
sql = "TRUNCATE TABLE book"
cursor.execute(sql)

# 크롤링을 통해 책 제목 가져오기
titles = get_book_titles()
print(titles)

# Database Insert
sql = "INSERT INTO book (title, detail) VALUES (%s, %s)"
for title in titles:
    cursor.execute(sql, (title, "안녕안녕 나는 지수야~ 헬륨가스 먹었더니 요로케 됐찌~"))

db.commit()
db.close()
