from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import Http404
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views import generic
from .models import Author, Book
from .forms import BookForm


def home_redirect(request):
    return redirect('home')


def home(request):
    return render(request, 'books/home.html')


def signup_user(request):
    if request.method == "GET":
        return render(request, "auth/signup.html", {'form': UserCreationForm()})
    else:
        if request.POST["password"] == request.POST["password_confirmation"]:
            try:
                user = User.objects.create_user(request.POST["username"], password=request.POST["password"])
                user.save()
                login(request, user)
                return redirect("authors")
            except IntegrityError:
                return render(request, "auth/signup.html", {'form': UserCreationForm(), 'error': 'That username has already been taken! Please choose another one'})
        else:
            return render(request, "auth/signup.html", {'form': UserCreationForm(), 'error': 'Passwords didn\'t match'})


def login_user(request):
    if request.method == "GET":
        return render(request, "auth/login.html", {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "auth/login.html", {'form': AuthenticationForm(), 'error': 'Username or password did\'t match'})
        else:
            login(request, user)
            return redirect("authors")


@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")


@login_required
def books_list_from_user(request):
    authors = Author.objects.filter(user=request.user)
    books = []

    for author in authors:
        book = Book.objects.filter(author=author)
        if book:
            books.extend(book)

    return render(request, "books/books.html", {'books':books})


@login_required
def finished_books_from_user(request):
    authors = Author.objects.filter(user=request.user)
    books = []

    for author in authors:
        book = Book.objects.filter(author=author, done=True)
        if book:
            books.extend(book)

    return render(request, "books/finished_books.html", {'books': books})


@login_required
def books_in_progress_from_user(request):
    authors = Author.objects.filter(user=request.user)
    books = []

    for author in authors:
        book = Book.objects.filter(author=author, in_process=True)
        if book:
            books.extend(book)

    return render(request, "books/inprogress_books.html", {'books': books})


@login_required
def book_create(request):
    if request.method == "GET":
        return render(request, "books/create_book.html", {'form': BookForm({'request': request})})
    else:
        try:
            form = BookForm(request.POST)
            new_book = form.save(commit=False)
            new_book.save()
            return redirect('books_list')
        except ValueError:
            return render(request, "books/create_book.html", {'form': BookForm(), 'error': 'Bad data passed in. Try again!'})


@login_required
def book_update(request, pk):
    if request.method == "GET":
        book = Book.objects.get(pk=pk)
        return render(request, "books/update_book.html", {'form': BookForm()})
    else:
        try:
            form = BookForm(request.PUT)
            updated_book = form.save(commit=False)
            updated_book.save()
            return redirect('books_list')
        except ValueError:
            return render(request, "books/update_book.html", {'form': BookForm(), 'error': 'Bad data passed in. Try again!'})


@login_required
def book_details(request, pk):
    book_author = None
    book = Book.objects.get(pk=pk)
    trigger = False

    for author in Author.objects.filter(user=request.user):
        if book.author == author:
            book_author = author
            trigger = True
            break

    if trigger:
        return render(request, "books/book.html", {'book': book, 'author': book_author})
    else:
        raise Http404


@login_required
def book_delete(request, pk):
    book = Book.objects.get(pk=pk)
    trigger = False

    for author in Author.objects.filter(user=request.user):
        if book.author == author:
            trigger = True
            break;

    if trigger:
        if request.method == "GET":
            return render(request, "books/delete_book.html", {'book':book})
        else:
            book.delete()
            return redirect("books_list")
    else:
        raise Http404


class AuthorsListView(LoginRequiredMixin, generic.ListView):
    model = Author
    login_url = '/login/'
    redirect_field_name = 'login_user'
    template_name = 'books/authors.html'
    context_object_name = 'authors'

    def get_context_data(self, **kwargs):
        context = super(AuthorsListView, self).get_context_data(**kwargs)
        context['authors'] = Author.objects.filter(user=self.request.user)
        return context


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = 'books/author.html'
    context_object_name = 'author'
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.filter(author=kwargs.get('object'))
        return context


class AuthorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Author
    fields = ['name', 'surname']
    template_name = 'books/create_author.html'
    success_url = reverse_lazy('authors')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AuthorCreateView, self).form_valid(form)


class AuthorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Author
    template_name = 'books/delete_author.html'
    success_url = reverse_lazy('authors')

    def get_object(self):
        author = super(AuthorDeleteView, self).get_object()
        if author.user == self.request.user:
            return author
        else:
            raise Http404


class AuthorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Author
    fields = ['name', 'surname']
    template_name = 'books/update_author.html'

    def get_object(self):
        author = super(AuthorUpdateView, self).get_object()
        if author.user == self.request.user:
            return author
        else:
            raise Http404

    def form_valid(self, form):
        super(AuthorUpdateView, self).form_valid(form)
        return redirect('author_detail', self.kwargs['pk'])