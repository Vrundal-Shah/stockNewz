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

    def __repr__(self):
        return self.id


class StocksClient(object):
    def __init__(self, api_key):
        self.sess = requests.Session()
        # self.base_url = f"https://www.alphavantage.co/query?apikey={api_key}&"
        self.finnhub_client = finnhub.Client(api_key=api_key)
        print(self.finnhub_client.company_news('AAPL', _from="2020-06-01", to="2020-06-10"))

    def search(self, ticker, start_date, end_date):
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

        result = []

        ## We may have more results than are first displayed
        for item_json in data:
            result.append(News(item_json))

        print('========================-----------------========================')
        print(result)
        return result

    def retrieve_movie_by_id(self, imdb_id):
        """
        Use to obtain a Movie object representing the movie identified by
        the supplied imdb_id
        """
        movie_url = self.base_url + f"i={imdb_id}&plot=full"

        resp = self.sess.get(movie_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        if data["Response"] == "False":
            raise ValueError(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')

        movie = Movie(data, detailed=True)

        return movie


## -- Example usage -- ###
if __name__ == "__main__":
    import os

    client = StocksClient(os.environ.get("API_KEY"))

    movies = client.search("guardians")

    for movie in movies:
        print(movie)

    print(len(movies))
