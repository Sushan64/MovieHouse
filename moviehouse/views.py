from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.conf import settings
from .models import Post, UserProfile
from .forms import PostForm, UserRegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib import messages
#from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
#from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .utils.tmdb import get_tmdb

#API
import requests
url_genre ="https://api.themoviedb.org/3/genre/movie/list" #type of genres list
headers_main = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_API_KEY}"
}
url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc"

data = get_tmdb(url, cache_key='results')
results = data.get('results', [])

data_genre = get_tmdb(url_genre, cache_key="genres_lookup", timeout=604800)

results_genres = data_genre["genres"]

genres_lookup = {genre['id']: genre['name'] for genre in results_genres} 
# ^ initialized genres_lookup as new dict with id as key and name as value

#------------------------

#Title to Slug convertor
def title_to_slug(title):
  slug = slugify(title)
  return slug

#------------------------

#Catch movie from ID
def get_movie_by_id(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    data = get_tmdb(url, cache_key=f"get_movie_by_id_{movie_id}")
    return data

#------------------------

#get_cast
def get_cast(movie_id):
  url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
  data = get_tmdb(url, cache_key=f'get_cast_{movie_id}')
  return data

#------------------------

#Pagination
def pagination(url, page=1, with_genre = None):
  try:
    page = int(page)
  except ValueError:
    page = 1

  params = {
    'page': page,
    'with_genre': with_genre
  }
  data = requests.get(url, headers = headers_main, params = params).json()
  total_pages = data.get('total_pages', 1)
  results = data.get('results', [])

  pagination_info = {
        'current_page': page,
        'total_pages': total_pages,
        'has_previous': page > 1,
        'has_next': page < total_pages,
        'previous_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < total_pages else None,
        'page_range': range(max(1, page - 2), min(total_pages + 1, page + 3)),
    'results': results
}
  return pagination_info

# Create your views here.
genres_to_show = {
  28: 'Action',
  35: 'Comedy',
  27: 'Horror',
  878: 'Sci-Fi'
}

industries = {
  "bollywood": "hi",
  "hollywood": "en",
  "popular": ""
}

def home(request):
  genre_movies = {}
  for genre_id, genre_name in genres_to_show.items():
    url = f"https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&with_genres={genre_id}"
    params = {
      'pages': 1
    }
    response = get_tmdb(url, cache_key=f"genres_movies_{genre_id}", params=params)
    genre_movies[genre_name] = response.get('results', [])
    
  industries_type =['popular', 'bollywood', 'hollywood'] #align it accordingly
  industries_data = {}
  for industry in industries_type:
    lang = industries.get(industry, 'en')
    industry_url = f"https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&with_original_language={lang}"
    movies = get_tmdb(industry_url, cache_key=f"industries_data_{lang}").get('results', [])
    industries_data[industry] = movies
    
  context = {
    'results': results,
    'genres_lookup': genres_lookup,
    'genre_movies': genre_movies,
    'genres_to_show': genres_to_show,
    'industries': industries_data
            }
  
  return render(request, 'moviehouse/home.html', context)

#------------------------

@login_required
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
    if len(query) > 50:
      pagination_data = {}
      movies= []
    else: 
      url = f'https://api.themoviedb.org/3/search/movie?query={query}'
      page = request.GET.get('page', 1)
      pagination_data = pagination(url, page)
      movies = pagination_data.get('results', [])

    context={'query':query,
           'movies': movies,
           'pagination': pagination_data
  }
    return render(request, 'moviehouse/search.html', context )
  return render(request, 'moviehouse/404.html')

#------------------------

def category(request, id, category):
  url = f"https://api.themoviedb.org/3/discover/movie?with_genres={id}&sort_by=popularity.desc"
  page = request.GET.get('page', 1)
  pagination_data = pagination(url, page)
  results = pagination_data.get('results', [])
  
  context = {'results': results,
             'genres_lookup':
             genres_lookup, "id": id,
             "category": category,
            "pagination": pagination_data}
  
  return render(request, 'moviehouse/category.html', context)

#------------------------

def indust(request, industry):
  page = request.GET.get('page', 1)
  if industry.lower() in industries:
    lang = industries.get(industry, 'en')
    url = f"https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&with_original_language={lang}"
    pagination_data = pagination(url, page)
    movies = pagination_data.get('results', [])
    context={"movies": movies,
             "industry": industry,
            'pagination': pagination_data}
    return render(request,"moviehouse/industries.html", context)
  return render(request, "moviehouse/404.html")

#--------------------------
#Post/Registration
def post(request, slug):
  post = get_object_or_404(Post, slug=slug)
  return render(request, 'moviehouse/post.html', {'post': post})

#--------------------------

@login_required
@staff_member_required
def create_post(request):
  if request.method == "POST":
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = form.save()
      post.save()
      messages.success(request, 'Post Successful!')
      return redirect('post', slug=post.slug )
  else:
    form = PostForm()
  return render(request, 'moviehouse/create_post.html', { 'form': form })
  

#-------------------
def register(request):
  if request.user.is_authenticated:
    return redirect('profile')
  if request.method == "POST":
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit = False)
      user.set_password(form.cleaned_data["password1"])
      user.save()
      login(request, user)
      messages.success(request, f"Your account has been created! You are now logged in")
      return redirect('profile')
  else:
    form = UserRegistrationForm()
  return render(request, "registration/register.html", {'form': form })

#--------------------

@login_required
def edit_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    #Initiallizing Form and Password
    form = UserProfileForm(instance=profile)
    password_form = PasswordChangeForm(user)
    
    if request.method == "POST":
        if request.POST.get('form_type') == 'profile':
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                user.first_name = request.POST.get('first_name', '')
                user.last_name = request.POST.get('last_name', '')
                user.save()
                messages.success(request, 'Your account has been successfully updated')
                return redirect('profile')
            else:
              messages.error(request, "Something went wrong! Couldn't update your profile")
              
              password_form = PasswordChangeForm(user)
            
        elif request.POST.get('form_type') == 'password':
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user) #Prevent user from logout
                messages.success(request, 'Password update successful')
                return redirect('profile')
            else:
                messages.error(request, "Something went wrong! Couldn't update your password")
                form = UserProfileForm(instance=profile)

    context = {
      'profile': profile,
        'form': form,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'password_form': password_form,
    }
    return render(request, 'profile/edit_profile.html', context)

#------------------
def custom_login(request):
  if request.user.is_authenticated:
    return redirect('profile')

  form = AuthenticationForm(request, data=request.POST or None)

  if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back! {user}')
            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, 'Invalid username or password')
          
  return render(request, 'registration/login.html', {'form': form})

#----------------------
def custom_logout(request):
  if request.method == "POST":
    logout(request)
    messages.success(request, 'You have been successfully logged out')
    return redirect('login')
  return redirect('profile')

#---------------------
def custom_404_view(request, exception):
  return render(request, "moviehouse/404.html", status=404)

#---------------------
#Forget Password Security Setup
#Default django PasswordResetView
class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/reset_password.html'
    html_email_template_name = 'registration/reset_password_email.html'
    email_template_name = 'registration/reset_password_email.html'
  
    # Default function of the class
    def form_valid(self, form):
        self.request.session['pwd_reset_step'] = 'email_sent' #Adding a New key on request.session dict with value 'email_sent'
        return super().form_valid(form) #Returning default django form but with a temp key in request.session

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
  # Default function of the class
  def dispatch(self, request, *args, **kwargs):
    # Check newly added key of request.session is available
    if request.session.get('pwd_reset_step') != 'email_sent':
      messages.info(request, 'Please enter your email to reset password.')
      return redirect('password_reset')
    # If exist then
    return super().dispatch(request, *args, **kwargs)

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
  def form_valid(self, form):
    # Change the value of key
    self.request.session['pwd_reset_step'] = 'completed'
    return super().form_valid(form)

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
  def dispatch(self, request, *args, **kwargs):
    # Check temp key exist
    if request.session.get('pwd_reset_step') != 'completed':
      messages.info(request, 'Please complete the password reset process.')
      return redirect('password_reset')
    # If exist then
    request.session.pop('pwd_reset_step', None)  # Clear after use
    return super().dispatch(request, *args, **kwargs)



#-------------
from cloudinary_storage.storage import MediaCloudinaryStorage

@csrf_exempt
@require_POST
def custom_ckeditor_upload(request):
    uploaded_file = request.FILES.get('upload')
    if not uploaded_file:
        return JsonResponse({"error": {"message": "No file was sent."}}, status=400)
    try:
        cloudinary_storage = MediaCloudinaryStorage()
        file_name = cloudinary_storage.save(uploaded_file.name, uploaded_file)
        file_url = cloudinary_storage.url(file_name)
        return JsonResponse({'url': file_url})
    except Exception as e:
        return JsonResponse({"error": {"message": f"Upload failed: {e}"}}, status=500)