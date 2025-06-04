from django.contrib import admin
from django.urls import *
from .views import *

app_name = 'films'

urlpatterns = [
    re_path('^A.{1}!/$',regular_films,name='regular_films' ),
    path('allfilms/',get_all_films,name='all'),
    path('slug/<slug:slug>/',get_film_by_slug,name='film-by-slug'),
    path('pk/<int:pk>/',get_film_by_id,name='film-by-id'),
    # path('add/',add_film,name='add_film'),
    # path('add/save/',add_saved_film,name='add_saved_film'),
    path('addfilm/',add_and_save_film,name='add_and_save_film'),
    path('index/',index,name='index'),
    # path('film-create/<str:method>/',film_create, name='film-create'),
    # path('film-create-html/<str:method>/', film_create_html),
    path("create/<str:method>/", Film_Create.as_view(), name="film_create"),
    path("create_html/<str:mode>/", Film_Create_html.as_view(), name="film_create_html"),
    path("by-release/", FilmByReleaseDate.as_view(), name="films_by_release"),
    path("by-created/", FilmListByCreatedAt.as_view(), name="films_by_created"),
]



