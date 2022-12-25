# next -> value="arrow_forward_ios"
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


url = "https://opensea.io/rankings"
pages = 3

browser = webdriver.Chrome()
browser.get(url)

linkSet = set()

temp_height = 0

for i in range(pages):
    time.sleep(1)
    while True:
        # 循环将滚动条下拉
        browser.execute_script("window.scrollBy(0,1000)")
        # sleep一下让滚动条反应一下

        time.sleep(3)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        element = soup.find(role="table")

        rows = element.find_all(role="row")

        for row in rows:
            linkSet.add(row['href'])

        # 获取当前滚动条距离顶部的距离
        check_height = browser.execute_script(
            "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        # 如果两者相等说明到底了
        if check_height == temp_height:
            break
        temp_height = check_height

    nextBtn = browser.find_element(
        by=By.XPATH, value="//i[@value='arrow_forward_ios']")
    nextBtn.click()


print(linkSet)
print(len(linkSet))
