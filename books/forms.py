from django import forms
from .models import Book, Author

class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Author not selected"
        self.fields['author'].queryset = Author.objects.filter(user=args[0]['request'].user)

    class Meta:
        model = Book
        fields = ['author', 'title', 'description', 'pages', 'done', 'in_process']