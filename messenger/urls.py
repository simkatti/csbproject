from django.urls import path
from .views import indexPage, loginPage, signupPage, logoutView, deleteView, homePage, NewMessage, searchMessages


urlpatterns = [
    path('', indexPage, name='index'),
    path('login/', loginPage, name='login'),
    path('signup/', signupPage, name='signup'),
    path('logout/', logoutView, name= 'logout'),
    path('delete/', deleteView, name='delete'),
    path('home/', homePage, name='home'),
    path('newmessage/', NewMessage, name='newmessage'),
    path('search/', searchMessages, name='search' )

]
