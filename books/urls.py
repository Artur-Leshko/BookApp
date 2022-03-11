from django.urls import path
from books import views

urlpatterns = [
    #Homepage
    path('', views.home_redirect, name="redirect"),
    path('home/', views.home, name="home"),

    #Auth
    path('signin/', views.signup_user, name="signup_user"),
    path('login/', views.login_user, name="login_user"),
    path('logout/', views.logout_user, name="logout_user"),

    #Authors
    path('authors/', views.AuthorsListView.as_view(), name="authors"),
    path('authors/create/', views.AuthorCreateView.as_view(), name="author_create"),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name="author_detail"),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name="author_delete"),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name="author_update"),

    #Books
    path('books/', views.books_list_from_user, name="books_list"),
    path('books/finished/', views.finished_books_from_user, name="finished_books"),
    path('books/in-progress/', views.books_in_progress_from_user, name="inprogress_books"),
    path('books/create/', views.book_create, name="book_create"),
    path('books/<int:pk>/', views.book_details, name="book_detail"),
    path('books/<int:pk>/delete/', views.book_delete, name="book_delete"),
    path('books/<int:pk>/update/', views.book_update, name="book_update"),
]