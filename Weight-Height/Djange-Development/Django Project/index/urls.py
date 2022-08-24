from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.calculate,name='calculate'),
    path('index',views.index,name='index'),
    path('calculation',views.calculation,name='calculation'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('user_login',views.user_login,name='user_login'),
    path('all_result',views.all_result,name='all_result'),
]
