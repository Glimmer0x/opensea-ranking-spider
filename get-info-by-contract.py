from bs4 import BeautifulSoup
from selenium import webdriver
import json

chainOptions = [
    "arbitrum",
    "avalanche",
    "bsc",
    "ethereum",
    "klaytn",
    "optimism",
    "matic",
    "solana"
]


def getInfoByContract(address, chain):
    assert chain in chainOptions, "chain must be one of the following: " + \
        ", ".join(chainOptions)

    try:
        url = f"https://opensea.io/assets/{chain}/{address}/6"
        browser = webdriver.Chrome()
        browser.get(url)

        soup = BeautifulSoup(browser.page_source, 'html.parser')

        element = soup.find(id="__NEXT_DATA__")
        content = element.string
        data = json.loads(content)

        nft = data["props"]["ssrData"]["nft"]
        assetContract = nft["assetContract"]
        nftAddress = assetContract["address"]
        nftChain = assetContract["chain"]

        collection = data["props"]["ssrData"]["nft"]["collection"]
        name = collection["name"]
        slug = collection["slug"]
        description = collection["description"]

        return {"contractAddress": nftAddress, "chain": nftChain, "name": name, "opensea-slug": slug, "description": description}
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    address = "0x7f7e28d1d79eebd3c3e17539934e723a14bfe97a"
    chain = "matic"
    print(getInfoByContract(address, chain))
