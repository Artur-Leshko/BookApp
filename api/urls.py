from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.AuthorsList.as_view()),
    path('authors/<int:pk>/', views.AuthorsRetrieveUpdateDestroy.as_view()),
    path('books/', views.BooksList.as_view()),
    path('books/<int:pk>/', views.BooksRetrieveUpdateDestroy.as_view()),

    path('signup/', views.signup),
]