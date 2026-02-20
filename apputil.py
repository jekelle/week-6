import requests
import pandas as pd


class Genius:
    BASE_URL = "https://api.genius.com"

    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def _make_request(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}")

        return response.json()

    def search(self, search_term):
        return self._make_request("/search", params={"q": search_term})

    def get_artist(self, search_term):
        json_data = self.search(search_term)
        hits = json_data["response"]["hits"]

        if not hits:
            raise ValueError(f"No results found for {search_term}")

        artist_id = hits[0]["result"]["primary_artist"]["id"]

        return self._make_request(f"/artists/{artist_id}")

    def get_artists(self, search_terms):
        rows = []

        for term in search_terms:
            artist_json = self.get_artist(term)
            artist_info = artist_json["response"]["artist"]

            rows.append({
                "search_term": term,
                "artist_name": artist_info.get("name"),
                "artist_id": artist_info.get("id"),
                "followers_count": artist_info.get("followers_count"),
            })

        return pd.DataFrame(rows)
