import requests
import finnhub
from datetime import datetime

class News(object):
    def __init__(self, alpha_json, detailed=False):
        # if detailed:
            # self.genres = omdb_json["Genre"]
            # self.director = omdb_json["Director"]
            # self.actors = omdb_json["Actors"]
            # self.plot = omdb_json["Plot"]
            # self.awards = omdb_json["Awards"]

        # self.title = omdb_json["Title"]
        # self.year = omdb_json["Year"]
        # self.imdb_id = omdb_json["imdbID"]
        # self.type = "Movie"
        # self.poster_url = omdb_json["Poster"]
        self.headline = alpha_json["headline"]
        self.url = alpha_json["url"]
        # convert "datetime": 1569526180 to datetime object
        self.datetime = datetime.fromtimestamp(alpha_json["datetime"])
        print('self.datetime', self.datetime)
        self.id = str(alpha_json["id"])
        self.source = alpha_json["source"]
        self.image = alpha_json["image"]
        self.summary = alpha_json["summary"]
        self.related = alpha_json["related"]
        self.is_bookmarked = alpha_json['is_bookmarked']

    def __repr__(self):
        return self.id
    
    def __dict__(self):
        return {
            "headline": self.headline,
            "url": self.url,
            "datetime": self.datetime,
            "id": self.id,
            "source": self.source,
            "image": self.image,
            "summary": self.summary,
            "related": self.related
        }


class StocksClient(object):
    def __init__(self, api_key):
        self.sess = requests.Session()
        # self.base_url = f"https://www.alphavantage.co/query?apikey={api_key}&"
        self.finnhub_client = finnhub.Client(api_key=api_key)
        print(self.finnhub_client.company_news('AAPL', _from="2020-06-01", to="2020-06-10"))

        # contain the latest search results
        self.search_results = []

    def search(self, ticker, start_date, end_date, current_user):
        """
        Searches the API for the supplied search_string, and returns
        a list of Media objects if the search was successful, or the error response
        if the search failed.

        Only use this method if the user is using the search bar on the website.
        """
        # page = 1

        # search_url = f"function=NEWS_SENTIMENT&tickers={tickers}"

        # resp = self.sess.get(self.base_url + search_url)
        data = self.finnhub_client.company_news(ticker, _from=start_date, to=end_date)

        # if resp.status_code != 200:
        #     raise ValueError(
        #         "Search request failed; make sure your API key is correct and authorized"
        #     )

        # data = resp.json()
        print('data', data)
        # if "Information" in data:
        #     raise ValueError(f'[ERROR]: Error retrieving results: \'{data["Information"]}\' ')

        # search_results_json = data["feed"]

        self.search_results = []

        ## We may have more results than are first displayed
        for item_json in data:
            if current_user is not None and str(item_json["id"]) in current_user.saved_news:
                print(item_json['headline'])
                item_json["is_bookmarked"] = 0
            else:
                item_json["is_bookmarked"] = 1
            self.search_results.append(News(item_json))

        return self.search_results
    
    def get_news_by_id(self, news_id):
        """
        Use to obtain a News object representing the news article identified by
        the supplied news_id
        """
        print([item.id for item in self.search_results])
        item_found = False
        for item in self.search_results:
            if item.id == news_id:
                news_data = item
                item_found = True
                break
        if not item_found:
          raise ValueError(f"News with id {news_id} not found")

        return news_data.__dict__()
    
    def get_ticker_basic_financials(self,ticker):
        data=self.finnhub_client.company_basic_financials(ticker, 'all')
        return data


## -- Example usage -- ###
if __name__ == "__main__":
    import os

    client = StocksClient(os.environ.get("API_KEY"))

    movies = client.search("guardians")

    for movie in movies:
        print(movie)

    print(len(movies))
