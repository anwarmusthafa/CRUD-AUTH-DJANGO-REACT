from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.hello_world, name="index" ),
    path('person/', views.person, name="person" ),
     path('person/<int:pk>/', views.person_detail, name="person_detail"),
     path('signup/', views.signup, name='signup'),
     path('signin/', views.signin, name='signin'),
     path('signout/', views.signout, name='signout'),
]
