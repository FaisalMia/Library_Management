from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView,HomeView,homePage,DetailsPostView,CommentsPostView,profile_view,Return_Book,add_book, add_book_category
 
urlpatterns = [
    path('register/',UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('home/', homePage, name='homepage'),
    path('book/<slug:book_slug>/',homePage, name='book_wise_post'),
    path('detail/<int:id>/',DetailsPostView.as_view(),name='detail'),
    path('details/<int:id>/',CommentsPostView.as_view(),name='detail_post'),
    path('profile/<int:id>/',profile_view, name='profile'), 
    path('return/<int:id>/',Return_Book, name='return_book'),
    path('add-book/', add_book, name='add_book'),
    path('add-category/', add_book_category, name='add_book_category'),
]