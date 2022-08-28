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
from books.models import Book, BookComment, Category, InBoxMessages, BookReview, BookRentHistory, Author
from books import form, models
from books.form import ContactForm, CommentForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, FormView, TemplateView
from books.form import ProfileUpdateForm, UserRegisterForm, UserUpdateForm


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'
    success_message = "Now you are registered, try to log in!"


class UserDetailView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = 'users/user_detail.html'


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    login_url = "login"
    form_class = UserUpdateForm
    p_form = ProfileUpdateForm()
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('UserProfile')
    success_message = "Now your profile is updated!"

    def form_valid(self, form):
        self.request.user.username = self.request.POST['username']
        self.request.user.email = self.request.POST['email']
        self.request.user.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super(UserUpdateView, self).get_initial()
        initial['username'] = self.request.user.username
        initial['email'] = self.request.user.email
        return initial


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    login_url = "login"
    form_class = ProfileUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('UserProfile')
    success_message = "Now you photo is updated"

    def form_valid(self, form):
        if 'image' in self.request.FILES:
            self.request.user.profile.image = self.request.FILES['image']
            self.request.user.profile.save()
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.INFO,
                                 'Your profile pic is not change')
            return HttpResponseRedirect(reverse_lazy('UserProfile'))

    def get_initial(self):
        initial = super(ProfileUpdateView, self).get_initial()
        initial['image'] = self.request.user.profile.image
        return initial


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
    # model = models.Book
    # fields = ['name', 'authors', 'status']
    success_url = reverse_lazy('book_index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        name = form.cleaned_data['name']

        book = models.Book(name=name)
        book.save()

        # author_list = models.Author.objects.filter(pk__in=author)
        # print(author_list)
        for author in form.cleaned_data['authors']:
            book.authors.add(author)
        print(book.authors.all())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_book'] = 'active'
        return context


class BookUpdate(UpdateView):
    template_name = 'book/update.html'
    form_class = form.BookForm
    model = models.Book
    #fields = ['name', 'authors', 'status']
    success_url = reverse_lazy('book_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_book'] = 'active'
        return context


class BookDelete(DeleteView):
    model = models.Book
    success_url = reverse_lazy('book_index')

    # return without confirmation template
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class HomeListView(ListView):
    template_name = 'book/home.html'
    model = Book

    def get_queryset(self):
        queryset = super(HomeListView, self).get_queryset()
        return queryset.all().order_by('-id')[:9]


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


class SearchBookListView(ListView):
    template_name = "book/search.html"
    model = Book

    def get_queryset(self):
        queryset = super(SearchBookListView, self).get_queryset()
        q = self.request.GET.get("name", "")
        if q:
            book_by_name = queryset.filter(name__icontains=q)
            book_by_authors = queryset.filter(authors__icontains=q)
            return book_by_authors | book_by_name
        return queryset


class BookDetailView(FormMixin, DetailView):
    template_name = "book/book_detail.html"
    model = Book
    form_class = CommentForm

    def get_success_url(self):
        return reverse('bookDetail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = BookComment.objects.filter(book=self.object).order_by('-id')
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


@login_required(login_url='login')
def login_to_comment_redirect(request, pk):
    return redirect('bookDetail', pk=pk)


@login_required(login_url='login')
def confirm_rent_view(request, pk):
    try:
        b = Book.objects.get(pk=pk)
        if b.book_amount <= 0:
            messages.warning(
                request, f'You cant rent this book')
            return redirect('bookDetail', pk=b.pk)
    except Book.DoesNotExist:
        raise Http404("We ont have this book")
    return render(request, 'book/confirm_rent.html', {'book': b})


@login_required(login_url='login')
def rent_book_view(request, pk):
    try:
        b = Book.objects.get(pk=pk)
        if b:
            if b.book_amount > 0:
                b.book_amount -= 1
                b.save()
                log_history = BookRentHistory(user=request.user, book=b)
                log_history.save()
                messages.success(
                    request, f'You rent a book: {b.name}')
            else:
                messages.warning(
                    request, f'You cant rent this book')
                return redirect('bookDetail', pk=b.pk)
    except Book.DoesNotExist:
        raise Http404("Book is unavailable")
    return redirect('UserProfile')


login_required(login_url='login')
def return_book_view(request, pk):
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
    
    def get_absolute_url(self):
        return reverse('article-view', args=(str(self.pk)))


@login_required(login_url='login')
def rate_book_view(request, pk, rating):
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
        return redirect('bookDetail', pk=b.pk)
    except Book.DoesNotExist:
        raise Http404("Book is unavailable")
    return redirect('bookDetail', pk=b.pk)


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
            return redirect('home')
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