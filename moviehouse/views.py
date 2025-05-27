from django.shortcuts import render

#API
import requests
def api():
  api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMjRkMDU1NGUwZGE4NjdhZGMwN2NiMTlmNDExYTBlYyIsIm5iZiI6MTc0ODI0MDk5MS45MzcsInN1YiI6IjY4MzQwYTVmNWY2NDcwNTNlNzA1NTIzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RRXStaFK8cRX1N26g69Qtl4GzmRS3Ebc0ygec1_kVCc'
  
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
  


# Create your views here.
def home(request):
  results, genres_lookup = api()
  return render(request, 'moviehouse/home.html', {'results': results, 'genres_lookup': genres_lookup})