# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
from tqdm import tqdm
import time
import pymysql
import config


def get_book_titles():
    # Initialize variables
    title_list = []
    detail_list = []

    maximum = 20

    # Set options for Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # Crawl each page for traditional fairy tales
    with webdriver.Chrome(options=chrome_options) as driver:
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

                # Switch to new tab
                driver.switch_to.window(driver.window_handles[-1])

                elements_content = driver.find_elements(By.CLASS_NAME, 'content')
                for element in elements_content:
                    element_text = element.text
                    detail_list.append(element_text)

                driver.close()

                # Switch back to original tab
                driver.switch_to.window(driver.window_handles[0])

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
# CREATE

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
