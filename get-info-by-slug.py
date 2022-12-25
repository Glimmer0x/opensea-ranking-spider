import requests


def getInfoBySlug(slug):
    try:
        url = f"https://api.opensea.io/collection/{slug}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "referer": "https://opensea.io/"
        }

        response = requests.get(url, headers=headers)
        collection = response.json()["collection"]

        name = collection["name"]
        symbol = collection["primary_asset_contracts"][0]["symbol"]
        contractAddress = collection["primary_asset_contracts"][0]["address"]
        description = collection["description"]
        social = {
            "discord": collection["discord_url"],
            "medium": collection["medium_username"],
            "twitter": collection["twitter_username"],
            "website": collection["external_url"],
            "telegram": collection["telegram_url"],
            "instagram": collection["instagram_username"],
            "wiki": collection["wiki_url"]
        }
        createdAt = collection["primary_asset_contracts"][0]["created_date"]

        return {
            "slug": slug,
            "name": name,
            "symbol": symbol,
            "contractAddress": contractAddress,
            "description": description,
            "social": social,
            "createdAt": createdAt
        }
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    slug = "nouns"
    print(getInfoBySlug(slug))
