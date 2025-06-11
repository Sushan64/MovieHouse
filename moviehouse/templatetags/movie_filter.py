from django import template
import random
from django.utils.text import slugify
from moviehouse.views import get_movie_by_id
from urllib.parse import urlencode

register = template.Library()

'''
@register.filter(name="movie_filter_10")
def filter_by_genre(movies, genre_id):
    filtered_movies = []
    for movie in movies:
        if genre_id in movie.get('genre_ids', []):
          filtered_movies.append(movie)
          if len(filtered_movies) >= 10:
              break
    return filtered_movies
'''

@register.filter(name="random")
def random_filter(movies):
    rand_choice = random.choice(movies)
    return rand_choice

@register.filter(name="get_item")
def get_item(dict, key):
    if not key:
        return dict
    return dict.get(key)

@register.filter(name="get_key")
def get_value(dict, value_item):
    for key, value in dict.items():
        if value == value_item:
            return key
    return dict


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

@register.filter(name="genre_icon")
def genre_icon(genre):
    icon ={
        'Action': "fas fa-fist-raised text-red-400",
        "Comedy": "fas fa-laugh text-yellow-400",
        "Adventure": "fas fa-mountain text-green-400",
        "Romance": "fas fa-heart text-pink-400",
        "Horror": "fas fa-ghost text-purple-400",
        "Sci-Fi": "fas fa-rocket text-blue-400",
        "Drama": "fas fa-theater-masks text-indigo-400",
    }
    
    return icon.get(genre, 'fas fa-film text-gray-400')

@register.filter(name="category_icon")
def category_icon(str):
    icons ={
        "popular":"fas fa-fire text-orange-500",
        "bollywood":"fa-solid fa-ticket",
        "hollywood": "fa-solid fa-star",
    }
    if str in icons:
        icon = icons.get(str)
        return icon
    return "fas fa-film text-gray-400"

@register.filter(name="preserve_query")
def preserve_query(params, exclude_key ="page"):
    query_dict =  params.copy()
    query_dict.pop(exclude_key, None)
    return query_dict.urlencode()

@register.simple_tag(takes_context=True)
def page_url(context, page_number):
    
    # Get a mutable copy of the current GET parameters from the request
    query_params = context['request'].GET.copy()
    if int(page_number) == 1:
        query_params.pop('page', None)
    else:
        query_params['page'] = page_number
    return query_params.urlencode()
