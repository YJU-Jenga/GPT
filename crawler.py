import pymysql
import requests
from bs4 import BeautifulSoup
import time
import config


def fetch_titles_and_details(page_number):
    url = f"http://18children.president.pa.go.kr/our_space/fairy_tales.php?srh%5Bcategory%5D=07&srh%5Bpage%5D={page_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = [title.text.strip().replace(" ", "") for title in soup.select(".title > a")]
    details = [content.text.strip() for content in soup.select(".txt > a")]
    return titles, details


def main():
    start = time.time()
    maximum_page = 20
    titles = []
    details = []
    for page_number in range(1, maximum_page + 1):
        page_titles, page_details = fetch_titles_and_details(page_number)
        titles.extend(page_titles)
        details.extend(page_details)
    end = time.time()

    print(f"{end - start:.5f} sec")
    print(titles)
    print(details)

    # Connect to database
    db = pymysql.connect(
        host='localhost',
        user='jenga',
        password=config.database_password,
        database='jenga',
        charset='utf8'
    )

    cursor = db.cursor()
    cursor.execute("TRUNCATE TABLE book")

    insert_query = "INSERT INTO book (title, detail) VALUES (%s, %s)"
    for title, detail in zip(titles, details):
        cursor.execute(insert_query, (title, detail))
    db.commit()
    db.close()


if __name__ == '__main__':
    main()
