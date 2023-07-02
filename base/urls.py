from django.urls import path
from . import views #We import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('',views.home,name="home"), #whenever user requests for any page, we call corresponing functions defined in views.py of this app. We also name these pages seperately just to classify among them.
    path('room/<str:pk>/',views.room,name="room"),#<str:pk> is dynamic url routing which directs to specific room in rooms.
    path('profile/<str:pk>/',views.userProfile, name="user-profile"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]