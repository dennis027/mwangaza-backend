from django.urls.conf import path,include
from . import views
from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *  
from rest_framework_jwt.views import obtain_jwt_token 

router = DefaultRouter()

router.register('user',UserViewSet,basename='user'),


urlpatterns=[
     path('',include(router.urls)),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

] 