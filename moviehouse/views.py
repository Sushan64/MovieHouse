from django.shortcuts import render
from django.utils.text import slugify
from django.conf import settings

#API
import requests
def api():
  api_key = settings.TMDB_API_KEY
  
  url_genre ="https://api.themoviedb.org/3/genre/movie/list?language=en"

  results = []
  headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}"
  }
  for pages in range(1, 4):
      url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
  
      headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}"
}
      params = {'page': pages}
      response = requests.get(url, headers=headers, params=params)
      data = response.json()
      results.extend(data["results"])
    
  
  genre_response = requests.get(url_genre, headers=headers)
  
  data_genre = genre_response.json()
  
  results_genres = data_genre["genres"]
  
  genres_lookup = {genre['id']: genre['name'] for genre in results_genres}  #initialized genres_lookup as new dict with id as key and name as value
  return results, genres_lookup


#Title to Slug convertor
def title_to_slug(title):
  slug = slugify(title)
  return slug

#Catch movie from ID
def get_movie_by_id(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


# Create your views here.
def home(request):
  results, genres_lookup = api()
  return render(request, 'moviehouse/home.html', {'results': results, 'genres_lookup': genres_lookup})

def movie_content(request, movie_id, slug):
  results, genres_lookup = api()
  movie = get_movie_by_id(movie_id)
  if not movie:
    return render(request, 'moviehouse/404.html')
  return render(request, 'moviehouse/movie_container.html', {'movie': movie, 'genres_lookup': genres_lookup})

def search(request):
  movies = []
  query = request.GET.get('search')
  if query:
    url = f'https://api.themoviedb.org/3/search/movie?query={query}'
    headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_API_KEY}"
    }
    
    params = {
      'page': 1
      
    }
    response = requests.get(url,headers =headers, params=params)
    data = response.json()
    movies = data.get('results', [])
    
  return render(request, 'moviehouse/search.html', {'query':query, 'movies': movies})