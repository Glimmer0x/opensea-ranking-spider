from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
from options import periodOptions, chainOptions, categoryOptions


def getSlugSetOfRank(pages, period, chain, category, display, browser=None):
    assert period in periodOptions  # check if period is valid
    assert pages > 0          # check if pages is valid
    assert chain in chainOptions  # check if chain is valid
    assert category in categoryOptions  # check if category is valid

    query = []
    if period:
        query.append(f"sortBy={period}")
    if chain:
        query.append(f"chain={chain}")
    if category:
        query.append(f"category={category}")
    query = "?"+"&".join(query)
    url = f"https://opensea.io/rankings{query}"
    print("Opening: "+url)

    if browser is None:
        browser = webdriver.Chrome()
        browser.set_page_load_timeout(10)
    if not display:
        browser.set_window_position(-10000, 0)
    browser.get(url)

    slugSet = set()

    height = 0
    page = 0

    while page < pages:
        time.sleep(1)
        while True:
            browser.execute_script("window.scrollBy(0,1000)")

            time.sleep(1)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            try:

                table = soup.find(role="table")
                if not table:
                    raise NoSuchElementException()

                rows = table.find_all(role="row")
                for row in rows:
                    collectionLink = row['href']
                    slug = collectionLink.split("/")[-1]
                    slugSet.add(slug)
            except NoSuchElementException as e:
                print("No table found! ULR: "+url)
                break

            check_height = browser.execute_script(
                "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            if check_height == height:
                break
            height = check_height

        page += 1

        try:
            nextBtnChild = browser.find_element(
                by=By.XPATH, value="//i[@value='arrow_forward_ios']")
            nextBtn = nextBtnChild.find_element(
                by=By.XPATH, value=('./..'))
            if nextBtn.is_enabled():
                nextBtn.click()
            else:
                break
        except NoSuchElementException as e:
            break

    return slugSet


if __name__ == "__main__":
    browser = webdriver.Chrome()
    # slugSet = getSlugSetOfRank(2, chain="avalanche", period="total_volume",
    #                            category="virtual-worlds", display=True, browser=browser)
    # print(slugSet)
    # print(len(slugSet))

    slugSet = getSlugSetOfRank(2, chain="solana", period="one_hour_volume",
                               category="trading-cards", display=True, browser=browser)
    print(slugSet)
    print(len(slugSet))
