from django.shortcuts import render
from django.utils.text import slugify
from django.conf import settings

#API
import requests
url_genre ="https://api.themoviedb.org/3/genre/movie/list"
headers_main = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_API_KEY}"
}
results = []
for pages in range(1, 4):
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc"
    headers = headers_main
    params = {'page': pages}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    results.extend(data["results"])
  
genre_response = requests.get(url_genre, headers=headers) 
data_genre = genre_response.json()

results_genres = data_genre["genres"] 
genres_lookup = {genre['id']: genre['name'] for genre in results_genres}  #initialized genres_lookup as new dict with id as key and name as value

#------------------------

#Title to Slug convertor
def title_to_slug(title):
  slug = slugify(title)
  return slug

#------------------------

#Catch movie from ID
def get_movie_by_id(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    headers = headers_main
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

#------------------------

#get_cast
def get_cast(movie_id):
  url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
  headers = headers_main
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
      return response.json()
  return {}

#------------------------

# Create your views here.
genres_to_show = {
  28: 'Action',
  35: 'Comedy',
  27: 'Horror',
  878: 'Sci-Fi'
}

def home(request):
  headers = headers_main
  genre_movies = {}
  for genre_id, genre_name in genres_to_show.items():
    url = f"https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&with_genres={genre_id}"
    params = {
      'pages': 1
    }
    response = requests.get(url, headers=headers, params=params).json()
    genre_movies[genre_name] = response.get('results', [])

  url_upcomming = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"

  upcoming_response = requests.get(url_upcomming, headers = headers_main).json()
  upcomming_movies = upcoming_response.get('results', [])
    
  context = {'results': results, 'genres_lookup': genres_lookup, 'genre_movies': genre_movies, 'upcomming_movies': upcomming_movies}
  
  return render(request, 'moviehouse/home.html', context)

#------------------------

def movie_content(request, movie_id, slug):
  
  movie = get_movie_by_id(movie_id)
  cast_data = get_cast(movie_id)
  casts = cast_data.get('cast', [])
  context ={
    'movie': movie,
    'genres_lookup': genres_lookup,
    'casts':casts
  }
  if not movie:
    return render(request, 'moviehouse/404.html')
  return render(request, 'moviehouse/movie_container.html', context)

#------------------------

def search(request):
  movies = []
  query = request.GET.get('search')
  if query:
    url = f'https://api.themoviedb.org/3/search/movie?query={query}'
    headers = headers_main
    params = {
      'page': 1
      }
    response = requests.get(url,headers =headers, params=params)
    data = response.json()
    movies = data.get('results', [])  
  return render(request, 'moviehouse/search.html', {'query':query, 'movies': movies})

#------------------------

def category(request, id, category):
  url = f"https://api.themoviedb.org/3/discover/movie?with_genres={id}&sort_by=popularity.desc"
  headers = headers_main
  params = {
    'pages' : 1
  }
  response= requests.get(url, headers=headers, params=params)
  data = response.json()
  results = data.get('results', [])
  
  context = {'results': results, 'genres_lookup': genres_lookup, "id": id, "category": category}
  
  return render(request, 'moviehouse/category.html', context)

#------------------------
