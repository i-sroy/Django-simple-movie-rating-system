from django.urls import path
from . import views



#urlpatterns is the name of the variable that cannot be changed as django looks for this particular variable
# while mapping views to urls
urlpatterns = [
   # path('hello/',views.say_hello),  # "playground/hello is the endpoint that will be given in the browser and views.say_hello is the reference to the function inside views.py that needs ti be called"
    #path('api-token-auth/', RegisterAPI.as_view())
    path('register/', views.RegisterAPI.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('logout/', views.LogoutAPI.as_view()),
    path('user_details/', views.GetCredentialsAPI.as_view()),
    path('edit_details/', views.EditDetailsAPI.as_view()),
    path('movie_details/', views.MovieDetailsAPI.as_view()),
    path('top_movies/', views.TopMoviesAPI.as_view()),
    path('rate/', views.RateAPI.as_view())
    

   
]