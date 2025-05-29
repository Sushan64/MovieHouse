from django.urls import path, include
from . import views

urlpatterns =[
  path('', views.home, name='home'),
  path('movie/<str:movie_id>/<str:slug>', views.movie_content, name="movie-detail"),
  path('movie/', views.search, name="search")
]