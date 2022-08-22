from django import forms
from . import models

STATUS = (
        ('w', 'Wypożyczona'),
        ('Z', 'Zwrócona'),
        ('N', 'Nie zwrócono'),
    )


class AuthorForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateTimeField(input_formats=['%Y-%m-%d'],
                                     widget=forms.DateTimeInput(attrs={'class': 'form-control'}, format='%Y-%m-%d'))

    class Meta:
        model = models.Author
        fields = ['first_name', 'last_name', 'birth_date']


class BookForm(forms.ModelForm):
    STATUS = (
        ('D', 'Dostępna'),
        ('N', 'Niedostępna'),
    )
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=STATUS, widget=forms.Select(attrs={'class': 'form-control'}))
    authors = forms.ModelMultipleChoiceField(queryset=models.Author.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = models.Book
        fields = ['name', 'authors', 'status', 'image', 'category']


class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.LibraryUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.LibraryUser
        fields = ['first_name', 'last_name', 'email', 'username']


class LendBookForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS, widget=forms.Select(attrs={'class': 'form-control'}))
    book = forms.ModelChoiceField(queryset=models.Book.objects.filter(status='D'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    library_user = forms.ModelChoiceField(queryset=models.LibraryUser.objects.all(),
                                          widget=forms.Select(attrs={'class': 'form-control'}))
    lend_date = forms.DateTimeField(input_formats=['%Y-%m-%d'],
                                    widget=forms.DateTimeInput(attrs={'class': 'form-control'}, format='%Y-%m-%d'))

    class Meta:
        model = models.BorrowBook
        fields = ['status', 'library_user', 'book', 'lend_date']


class LendBookUpdateForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS, widget=forms.Select(attrs={'class': 'form-control'}))
    return_date = forms.DateTimeField(input_formats=['%Y-%m-%d'],
                                      widget=forms.DateTimeInput(attrs={'class': 'form-control'}, format='%Y-%m-%d'), required=False)

    class Meta:
        model = models.BorrowBook
        fields = ['status', 'return_date']


class ContactForm(forms.Form):
    name = forms.CharField(label='Name')
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Message', widget=forms.Textarea())


class CommentForm(forms.Form):
    text = forms.CharField(label='Add comment:', widget=forms.Textarea(
        attrs={'rows': 4, 'cols': 15}))