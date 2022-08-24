from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, FormView, UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from books.models import Book, BookComment, Category, InBoxMessages, BookReview, BookRentHistory
from books import form, models
from books.form import ContactForm, CommentForm

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lendbooks'] = models.BorrowBook.objects.all()
        context['books_available'] = models.Book.objects.filter(status='D')
        context['active_index'] = 'active'
        return context


class AuthorIndex(TemplateView):
    template_name = 'author/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = models.Author.objects.all()
        context['active_author'] = 'active'
        return context


class AuthorCreate(CreateView):
    template_name = 'author/add.html'
    form_class = form.AuthorForm
    # model = models.Author
    # fields = ['first_name', 'last_name', 'birth_date']
    success_url = reverse_lazy('author_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_author'] = 'active'
        return context


class AuthorUpdate(UpdateView):
    template_name = 'author/update.html'
    form_class = form.AuthorForm
    model = models.Author
    # fields = ['first_name', 'last_name', 'birth_date']
    success_url = reverse_lazy('author_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_author'] = 'active'
        return context


class AuthorDelete(DeleteView):
    model = models.Author
    success_url = reverse_lazy('author_index')

    # return without confirmation template
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class BookIndex(TemplateView):
    template_name = 'book/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = models.Book.objects.all()
        context['active_book'] = 'active'
        return context


class BookCreate(CreateView):
    template_name = 'book/add.html'
    form_class = form.BookForm
    model = models.Book
    success_url = reverse_lazy('book_index')
    

class BookUpdate(UpdateView):
    template_name = 'book/update.html'
    form_class = form.BookForm
    model = models.Book
    # fields = ['name', 'authors', 'status']
    success_url = reverse_lazy('book_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_book'] = 'active'
        return context

class BookDetailView(FormMixin, DetailView):
    template_name = "book/books.html"
    model = Book
    form_class = CommentForm

    def get_success_url(self):
        return reverse('book_update', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = BookComment.objects.filter(
            book=self.object).order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        b = self.get_object()
        text = form.cleaned_data['text']
        new_comment = BookComment(text=text, book=b, user=self.request.user)
        new_comment.save()
        messages.success(self.request, "Your comment is added, thank you")
        return super().form_valid(form)

class BooksListView(ListView):
    template_name = 'book/books.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BooksListView, self).get_context_data(**kwargs)
        context.update({
            'top_3_books': Book.objects.order_by('-last_rating')[:3],
            'most_reviews': Book.objects.annotate(reviews_count=Count('reviews')).order_by('-reviews_count')[:3],
            'most_comments': Book.objects.annotate(comments_count=Count('comments')).order_by('-comments_count')[:3],
        })
        return context

    def get_queryset(self):
        return Book.objects.order_by('-id')[:3]

class BookDelete(DeleteView):
    model = models.Book
    success_url = reverse_lazy('book_index')

    # return without confirmation template
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class SearchBookListView(ListView):
    template_name = "book/search.html"
    model = Book

    def get_queryset(self):
        queryset = super(SearchBookListView, self).get_queryset()
        q = self.request.GET.get("q")
        if q:
            books_by_name = queryset.filter(name__icontains=q)
            books_by_author = queryset.filter(author__icontains=q)
            return books_by_author | books_by_name
        return queryset

class UserIndex(TemplateView):
    template_name = 'user/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = models.LibraryUser.objects.all()
        print(models.LibraryUser.objects.all())
        context['active_user'] = 'active'
        return context

class UserCreate(CreateView):
    template_name = 'user/add.html'
    form_class = form.UserForm
    # fields = '__all__'
    success_url = reverse_lazy('user_index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        models.LibraryUser.objects.create(user=user)

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_user'] = 'active'
        return context


class UserUpdate(UpdateView):
    template_name = 'user/update.html'
    form_class = form.UserUpdateForm
    model = models.LibraryUser
    # fields = '__all__'
    success_url = reverse_lazy('user_index')

    def get_initial(self):
        library_user = models.LibraryUser.objects.get(id=self.get_object().pk)
        user = User.objects.get(id=library_user.user.id)
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_user'] = 'active'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        library_user = models.LibraryUser.objects.get(id=self.get_object().pk)
        try:
            user = User.objects.get(id=library_user.user.id)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.save()
        except:
            pass

        return HttpResponseRedirect(self.get_success_url())


class UserDelete(DeleteView):
    model = models.LibraryUser
    success_url = reverse_lazy('user_index')

    # return without confirmation template
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class LendBookCreate(CreateView):
    template_name = 'borrowbook/add.html'
    form_class = form.LendBookForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        name = form.cleaned_data['book']
        models.Book.objects.filter(name=name).update(status='N')

        form.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_index'] = 'active'
        return context


class LendBookUpdate(UpdateView):
    template_name = 'borrowbook/update.html'
    form_class = form.LendBookUpdateForm
    model = models.BorrowBook
    # fields = ['status', 'return_date']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print(self.object.status)
        if self.object.status == 'D':
            models.Book.objects.filter(name=self.object.book.name).update(status='D')
        if self.object.status != 'D':
            models.Book.objects.filter(name=self.object.book.name).update(status='N')

        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_index'] = 'active'
        return context

@login_required(login_url='login')
def login_to_comment_redirect(request, pk):
    return redirect('book_update', pk=pk)


@login_required(login_url='login')
def confirm_rent(request, pk):
    try:
        b = Book.objects.get(pk=pk)
        if b.book_amount <= 0:
            messages.warning(
                request, f'You cant rent this book')
            return redirect('book_update', pk=b.pk)
    except Book.DoesNotExist:
        raise Http404("We ont have this book")
    return render(request, 'book/confirm_rent.html', {'book': b})


@login_required(login_url='login')
def rent_book(request, pk):
    try:
        b = Book.objects.get(pk=pk)
        if b:
            if b.book_amount > 0:
                b.book_amount -= 1
                b.save()
                log_history = BookRentHistory(user=request.user, book=b)
                log_history.save()
                messages.success(
                    request, f'You rent a book: {b.title}')
            else:
                messages.warning(
                    request, f'You cant rent this book')
                return redirect('book_update', pk=b.pk)
    except Book.DoesNotExist:
        raise Http404("Book is unavailable")
    return redirect('UserProfile')


@login_required(login_url='login')
def return_book(request, pk):
    try:
        b = Book.objects.filter(pk=pk)[0]
        if b:
            b.book_amount += 1
            b.save()
            log_history = BookRentHistory.objects.filter(book=b)[0]
            log_history.delete()
            messages.success(
                request, f'You successfully returned a book: {b.name}')
        else:
            messages.warning(
                request, f'Error occurs, sorry')
            return redirect('UserProfile')
    except Book.DoesNotExist:
        raise Http404("Book is unavailable now ")
    return redirect('UserProfile')


class CategoryBookListView(ListView):
    template_name = "book/category.html"
    model = Book

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        return Book.objects.filter(category=category)


@login_required(login_url='login')
def rate_book(request, pk, rating):
    try:
        b = Book.objects.get(pk=pk)
        if b and not(BookReview.objects.filter(user=request.user).filter(book=b)):
            review = BookReview(book=b, user=request.user, rating=rating)
            review.save()
            b.last_rating = b.calc_rating
            b.save()
            messages.success(
                request, f'You rated a book: {b.name}')

        else:
            messages.warning(
                request, f'You already rated this book')
        return redirect('book_update', pk=b.pk)
    except Book.DoesNotExist:
        raise Http404("Book is unavailable")
    return redirect('book_update', pk=b.pk)


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            new_message = InBoxMessages()
            new_message.name = name
            new_message.email = email
            new_message.message = message
            new_message.save()
            messages.success(request, "Your message is sent")
            return redirect('index')
    if request.user.is_authenticated:
        form = ContactForm()
        form.fields['name'].initial = request.user.username
        form.fields['email'].initial = request.user.email
        form.fields['message'].widget.attrs['placeholder'] = 'Write your message here'
        form.fields['name'].label = 'Login'
        form.fields['name'].widget.attrs['readonly'] = True
        form.fields['email'].widget.attrs['readonly'] = True
        return render(request, 'book/contact.html', {'form': form})
    else:
        form = ContactForm()
        form.fields['name'].widget.attrs['placeholder'] = 'Your name'
        form.fields['email'].widget.attrs['placeholder'] = 'Your email'
        form.fields['message'].widget.attrs['placeholder'] = 'Write your message here'
        return render(request, 'book/contact.html', {'form': form})