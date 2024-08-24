import requests


class NYTimesTopStoriesAPI:
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


# Ejemplo de uso
if __name__ == "__main__":
    # Reemplaza 'TU_CLAVE_DE_API' con tu clave de API de New York Times
    api_key = 'TU_CLAVE_DE_API'

    # Crea una instancia de la clase
    nytimes_api = NYTimesTopStoriesAPI(api_key)

    # Obtiene los titulares de las top stories
    top_stories = nytimes_api.get_top_stories()

    # Imprime los titulares
    if top_stories:
        for idx, headline in enumerate(top_stories, start=1):
            print(f"{idx}. {headline}")

    # Obtiene los resúmenes de las top stories
    top_abstracts = nytimes_api.get_top_abstracts()

    # Imprime los resúmenes
    if top_abstracts:
        for idx, abstract in enumerate(top_abstracts, start=1):
            print(f"{idx}. {abstract}")
