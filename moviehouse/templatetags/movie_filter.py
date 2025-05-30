from django import template
import random
from django.utils.text import slugify
from moviehouse.views import get_movie_by_id

register = template.Library()

@register.filter(name="movie_filter_10")
def filter_by_genre(movies, genre_id):
    filtered_movies = []
    for movie in movies:
        if genre_id in movie.get('genre_ids', []):
          filtered_movies.append(movie)
          if len(filtered_movies) >= 10:
              break
    return filtered_movies


@register.filter(name="random")
def random_filter(movies):
    rand_choice = random.choice(movies)
    return rand_choice

@register.filter(name="get_item")
def get_item(dict, key):
    if not key:
        return dict
    return dict.get(key)


@register.filter(name="slugify")
def slugify_title(title):
    slug = slugify(title)
    return slug

@register.filter(name="get_movie_by_id")
def get_movie(movie_id):
    movie = get_movie_by_id(movie_id)
    return movie

@register.filter(name="format_decimal")
def format_decimal(num):
    if num:
      num = int(num)
      formated = f"{num:.1f}"
      return formated
    return 0