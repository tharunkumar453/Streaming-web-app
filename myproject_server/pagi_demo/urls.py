from django.urls import path

from .views import MovieListView,MovieDetailsView,ReelsListView

urlpatterns = [
    path("movies/",MovieListView.as_view(),name="movie-list"),
    path("movies/<int:Movie_id>/",MovieDetailsView.as_view(), name="movie-details"),
    path("reels/",ReelsListView.as_view(),name="reel-list"),
]