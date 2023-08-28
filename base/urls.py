from django.urls import path
from .views import home, room, create_room, update_room, delete_room, login_page, logout_page

urlpatterns = [
    path('',home, name = "home" ), 
    path('room/<int:pk>', room, name = "room"),
    path('room/create', create_room, name = "create-room" ),
    path('room/update/<int:pk>', update_room, name = "update-room" ),
    path('room/delete/<int:pk>', delete_room, name = "delete-room" ),
    path('login', login_page, name = 'login'),
        path('logout', logout_page, name = 'logout')



]
