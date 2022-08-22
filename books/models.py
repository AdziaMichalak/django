from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image


class Category(models.Model):
    category = models.CharField(max_length=50)
    

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Imię')
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')
    birth_date = models.DateField(verbose_name='Data urodzenia')
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Book(models.Model):
    STATUS = (
        ('D', 'Dostępna'),
        ('N', 'Niedostępna'),
    )
    name = models.CharField(max_length=100, verbose_name='Tytuł')
    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name='Status')
    authors = models.ManyToManyField('Author', through='Authored', verbose_name='Autor')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    image = models.ImageField(default='default_book.png', upload_to='books_pics')
    
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Book, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (150, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    def __str__(self):
        return "%s" % self.name


class Authored(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)


class LibraryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return "%s %s (%s)" % (self.user.first_name, self.user.last_name, self.user.username)


def validate_lend(value):
    count_days = value - datetime.now().date()
    print(count_days.days)
    if count_days.days < 0:
        raise ValidationError(
            ('Liczna dni'),
            params={'value': value},
        )
    if count_days.days > 3:
        raise ValidationError(
            ('Może być wypożyczona tylko na maksymalnie 3 dni'),
            params={'value': value},
        )


class BorrowBook(models.Model):
    STATUS = (
        ('W', 'wypożyczona'),
        ('Z', 'Zwrócona'),
        ('N', 'Nie zwrócono'),
    )
    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name='Status')
    library_user = models.ForeignKey(LibraryUser, on_delete=models.SET_NULL, null=True, verbose_name='Użytkownik')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, verbose_name='Book')
    lend_date = models.DateField(validators=[validate_lend], verbose_name='Data wypożyczenia')
    return_date = models.DateField(null=True, blank=True, verbose_name='Data zwrotu')

    def __str__(self):
        return "%s %s" % (self.library_user.name, self.book.name)


class BookComment(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=300)


class InBoxMessages(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField(max_length=500)

    def __str__(self):
        return f'Message from {self.name}'