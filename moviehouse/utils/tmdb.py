import requests
from django.core.cache import cache
from django.conf import settings
import hashlib
from urllib.parse import urlencode

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_API_KEY}"
}

def get_tmdb(url, cache_key, params=None, timeout=300):

  params_string = urlencode(params or {})
  key_source = f"{cache_key}-{params_string}" if params_string else cache_key

  # Hash the full key to avoid special characters & length issues
  full_cache_key = hashlib.md5(key_source.encode()).hexdigest()
  
  data = cache.get(full_cache_key)
  if data:
    return data
    
  try:
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
      data = response.json()
      cache.set(full_cache_key, data, timeout)
      return data
  except requests.exceptions.RequestException as e:
    print(f'TMDB API error: {e}')
    
  return {}