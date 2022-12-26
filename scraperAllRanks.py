from options import periodOptions, chainOptions, categoryOptions
from scraperRank import getSlugSetOfRank
from selenium import webdriver
import time


def getAllSlugsInRanks(progress, display=False, browser=None):
    slugSet = set()
    allPages = float('inf')
    if browser is None:
        browser = webdriver.Chrome()
        browser.set_page_load_timeout(30)
    idx = 0

    for period in periodOptions:
        for chain in chainOptions:
            for category in categoryOptions:
                try:
                    if idx < progress:
                        idx += 1
                        continue
                    slugSet = slugSet | (getSlugSetOfRank(
                        allPages, period, chain, category, display=display, browser=browser))
                    idx += 1
                    time.sleep(2)
                    print(
                        f"Progress: {100*idx/(len(periodOptions)*len(chainOptions)*len(categoryOptions)):.2f} | Got {len(slugSet)} slugs so far.")
                except Exception as e:
                    print(e)
                    print(
                        f"Failed to get slugs for period={period}, chain={chain}, category={category}")
    return idx, slugSet


if __name__ == '__main__':
    import json

    with open('allSlugs.json', 'r') as f:
        data = json.load(f)
        progress = data["progress"]
        result = set(data["result"])

    new_progress, new_result = getAllSlugsInRanks(progress)

    with open('allSlugs.json', 'w') as f:
        json.dump({
            "progress": new_progress,
            "result": list(result | new_result)
        }, f)
