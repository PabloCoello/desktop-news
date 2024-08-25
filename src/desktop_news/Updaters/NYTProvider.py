import requests
from desktop_news.Register import Register
from desktop_news.IUpdater import IUpdater


@Register("Update prompt with latest news from New York Times news", tags=["news", "NYT"])
class NYTimesTopStoriesAPI(IUpdater):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.nytimes.com/svc/topstories/v2/home.json'

    def _make_request(self, params):
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def get_top_stories(self):
        params = {'api-key': self.api_key}
        data = self._make_request(params)
        if data:
            headlines = [article['title'] for article in data['results']]
            return headlines
        return None

    def get_top_abstracts(self):
        params = {'api-key': self.api_key}
        data = self._make_request(params)
        if data:
            abstracts = [article.get('abstract', 'N/A')
                         for article in data['results']]
            return abstracts
        return None

    def update(self) -> str:
        abstracts = self.get_top_abstracts()
        generated = ""
        for idx, abstract in enumerate(abstracts, start=1):
            generated += f"New: {abstract}\n"
        return generated

