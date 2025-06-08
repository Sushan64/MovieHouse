from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
  path('', views.home, name='home'),
  path('movie/<str:movie_id>/<str:slug>', views.movie_content, name="movie-detail"),
  path('movie/', views.search, name="search"),
  path('movie/<str:industry>', views.indust, name="industries"),
  path('<slug:slug>', views.post, name='post'),  path('category/<int:id>/<str:category>',views.category, name="category"),
  path('create/', views.create_post, name="create_post"),
  path('register/', views.register, name="register"),
  path('profile/', views.edit_profile, name="profile"),
  path('login/', views.custom_login, name="login"),
  path('logout/', views.custom_logout, name='logout'),
  
]