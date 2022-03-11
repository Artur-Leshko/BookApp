from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=255)
    pages = models.IntegerField(default=0)
    done = models.BooleanField(default=False)
    in_process = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title