# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import re
import time
import pymysql
import config


def get_book_titles():
    # Set Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # 브라우저가 뜨지 않고 실행됩니다.
    # chrome_options.add_argument("--disable-gpu") # Disable GPU rendering, 하드웨어 가속 안함.
    # chrome_options.add_argument("--lang=ko-Kr") # 사용언어 한국어
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Do not load images, 브라우저에서 이미지 로딩을 하지 않습니다.
    chrome_options.add_argument('--mute-audio')  # Mute audio, 브라우저에 음소거 옵션을 적용합니다.

    # Set maximum number of pages to crawl
    maximum = 20

    # Initialize title and detail lists
    title_list = []
    detail_list = []

    # Crawl each page for traditional fairy tales
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options) as driver:
        for i in tqdm(range(1, maximum + 1)):
            URL = f"http://18children.president.pa.go.kr/our_space/fairy_tales.php?srh%5Bcategory%5D=07&srh%5Bpage%5D={i}"
            driver.get(URL)

            # Wait for page to load
            driver.implicitly_wait(10)

            # Get all titles
            elements_title = driver.find_elements(By.CLASS_NAME, "title")
            for element in elements_title:
                titles = element.find_elements(By.TAG_NAME, "a")
                title = titles[0].text
                title_list.append(title)

            # Get all details
            for j in range(1, 6):
                detail = driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div[1]/ul/li[{j}]/dl/dt/a')
                detail.click()

                elements_content = driver.find_elements(By.CLASS_NAME, 'content')
                for element in elements_content:
                    element_text = element.text
                    detail_list.append(element_text)
                driver.back()

    # Remove non-Korean characters from titles
    title_replace = [re.sub(r"[^가-힣]", "", title) for title in title_list]
    return title_replace, detail_list


start = time.time()

# Connect to database
db = pymysql.Connect(
    host='localhost',
    user='jenga',
    password=config.database_password,
    database='jenga',
    charset='utf8',
)
cursor = db.cursor()

# Database Create Table
# create_table_query = """
# CREATE TABLE book (
#     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255),
#     detail TEXT
# )
# """

# cursor.execute(create_table_query)

# Clear book table in database
sql = "TRUNCATE TABLE book"
cursor.execute(sql)

# Get book titles and details
titles, details = get_book_titles()
print("Titles: ", titles)
print("Details: ", details)

# Insert titles and details into database
sql = "INSERT INTO book (title, detail) VALUES (%s, %s)"
for title, detail in zip(titles, details):
    cursor.execute(sql, (title, detail))
db.commit()
db.close()

end = time.time()

print(f"{end - start:.5f} sec")