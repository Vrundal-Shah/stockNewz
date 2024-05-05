import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import movie_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Review
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
        return redirect(url_for("stocks.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@stocks.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = movie_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


@stocks.route("/stocks/<movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    try:
        result = movie_client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        return render_template("movie_detail.html", error_msg=str(e))

    form = MovieReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            image=get_b64_img(current_user.username),
            movie_title=result.title,
        )

        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=movie_id)

    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews
    )


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