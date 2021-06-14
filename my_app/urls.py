from django.urls import path, include

from .import views  

urlpatterns = [
    path('', views.index),
    path('login',views.login),
    path('register',views.register),
    path('success', views.success),
    path('logout', views.logout),
    path('create_post', views.create_post),
    path('like/<int:id>',views.like),
]

#