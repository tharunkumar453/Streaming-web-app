from django.urls import path

from .views import (
    MovieListView,
    MovieDetailsView
    
)

urlpatterns = [
    path(
        "movies/",
        MovieListView.as_view(),
        name="movie-list"
    ),

    path(
        "movies/<int:Movie_id>/",
        MovieDetailsView.as_view(),
        name="movie-details"
    ),
]