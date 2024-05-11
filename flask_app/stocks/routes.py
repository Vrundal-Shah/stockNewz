import base64,io
from io import BytesIO
from datetime import datetime
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import stocks_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Review, News
from ..utils import current_time

stocks = Blueprint("stocks", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """


@stocks.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("stocks.query_results", ticker=form.ticker.data, start_date=form.start_date.data, end_date=form.end_date.data))

    return render_template("index.html", form=form)

@stocks.route("/save_news", methods=["GET"])
def save_news():
    news_id = request.args.get('news_id')
    next_url = request.args.get('next_url')

    if not news_id or not next_url:
        # Handle error: missing news_id or next_url
        return "Missing news ID or Next URL", 400  # Example error handling

    news_data = stocks_client.get_news_by_id(news_id)
    print('news_data', news_data)

    if news_data:
        print('news_data', news_data)
        existing_news = News.objects(news_id=news_data['id']).first()
        if existing_news is None:
            # Create the News model object and push to News collection in MongoDB
            new_news = News(
                headline=news_data['headline'],
                url=news_data['url'],
                datetime= news_data['datetime'],
                news_id=news_id,
                source=news_data['source'],
                image=news_data.get('image', "https://plus.unsplash.com/premium_photo-1688561383440-feef3fee567d?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTd8fG5ld3MlMjBtZWRpYXxlbnwwfHwwfHx8MA%3D%3D"),
                summary=news_data['summary'],
                related=news_data['related']
            )
            new_news.save()
    return redirect(next_url)

@stocks.route("/search-results/<ticker>/<start_date>/<end_date>", methods=["GET"])
def query_results(ticker, start_date, end_date):
    # ticker = request.args.get('ticker', default=None, type=str)
    # start_date = request.args.get('start_date', default=None, type=str)
    # end_date = request.args.get('end_date', default=None, type=str)
    try:
        if current_user.is_authenticated:
            results = stocks_client.search(ticker, start_date, end_date, current_user)
        else:
            results = stocks_client.search(ticker, start_date, end_date, None)
          
        company_basic_financials = stocks_client.get_ticker_basic_financials(ticker)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results, company_basic_financials=company_basic_financials)


# @stocks.route("/stocks/<movie_id>", methods=["GET", "POST"])
# def movie_detail(movie_id):
#     try:
#         result = stocks_client.retrieve_movie_by_id(movie_id)
#     except ValueError as e:
#         return render_template("movie_detail.html", error_msg=str(e))

#     form = MovieReviewForm()
#     if form.validate_on_submit():
#         review = Review(
#             commenter=current_user._get_current_object(),
#             content=form.text.data,
#             date=current_time(),
#             imdb_id=movie_id,
#             image=get_b64_img(current_user.username),
#             movie_title=result.title,
#         )

#         review.save()

#         return redirect(request.path)

#     reviews = Review.objects(imdb_id=movie_id)

#     return render_template(
#         "movie_detail.html", form=form, movie=result, reviews=reviews
#     )


@stocks.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    if not user:
        # If the user does not exist, you can choose to abort with a 404 error
        # or pass an error message to the template to display it differently
        return render_template("user_detail.html", error="User not found.")

    # Assuming a reverse lookup reference or a direct query to get the reviews by the user
    reviews = Review.objects(commenter=user)
    
    return render_template("user_detail.html", user=user, reviews=reviews, image=get_b64_img(username))
