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
    detail_list = []

    # 전래동화 크롤링
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options) as driver:
        for i in range(1, maximum + 1):
            URL = f"http://18children.president.pa.go.kr/our_space/fairy_tales.php?srh%5Bcategory%5D=07&srh%5Bpage%5D={i}"
            driver.get(URL)

            # 페이지 로딩 대기 (로딩이 완료되면 즉시 다음 코드 실행)
            driver.implicitly_wait(10)

            elements_title = driver.find_elements(By.CLASS_NAME, "title")

            # 동화 제목 크롤링
            for element in elements_title:
                titles = element.find_elements(By.TAG_NAME, "a")

                title = titles[0].text
                title_list.append(title)

            # 동화 내용 크롤링
            for j in range(1, 6):
                detail = driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div[1]/ul/li[{j}]/dl/dt/a')
                detail.click()

                elements_content = driver.find_elements(By.CLASS_NAME, 'content')

                for element in elements_content:
                    element_text = element.text
                    detail_list.append(element_text)
                driver.back()

    # 한글만 남게 하기
    title_replace = [re.sub(r"[^가-힣]", "", title) for title in title_list]
    return title_replace, detail_list


# Database
start = time.time()
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

# 크롤링을 통해 책 제목 및 내용 가져오기
titles, details = get_book_titles()
print("Titles: ", titles)
print("Details: ", details)



# Database Insert
sql = "INSERT INTO book (title, detail) VALUES (%s, %s)"
for title, detail in zip(titles, details):
    cursor.execute(sql, (title, detail))

db.commit()
db.close()

end = time.time()

print(f"{end - start:.5f} sec")
