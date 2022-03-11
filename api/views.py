from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from .serializers import AuthorSerializer, BookSerializer
from books.models import Author, Book
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError
from django.http import JsonResponse

@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(username=data["username"], password=data["password"])
            user.save()
            return JsonResponse({'token': 'asdsa'}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'That username has already been taken! Please choose another one'}, status=400)


class AuthorsList(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Author.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AuthorsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Author.objects.filter(user=user)

class BooksList(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        books = []
        for author in Author.objects.filter(user=self.request.user):
            book = Book.objects.filter(author=author)
            if author:
                books.extend(book)
        return books

    # def perform_create(self, serializer):
    #     serializer.save()

class BooksRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        books = []
        for author in Author.objects.filter(user=self.request.user):
            book = Book.objects.filter(author=author)
            if author:
                books.extend(book)
        return books