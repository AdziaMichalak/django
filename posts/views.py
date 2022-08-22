from django.shortcuts import render
from django.contrib import messages
from posts.models import Post, Author
from posts.forms import PostForm, AuthorForm
from django.contrib.auth.decorators import login_required


# Create your views here.

#@login_required
def posts_list(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            Post.objects.get_or_create(**form.cleaned_data)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Utworzono nowy post!"
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                form.errors['__all__']
            )

    form = PostForm()
    posts = Post.objects.all()
    title = 'Posty'
    return render(
        request=request,
        template_name="posts/list.html",
        context={"posts": posts, "title": title, "form": form}
    )


def post_details(request, id):
    post = Post.objects.get(id=id)
    title = 'Detale postu'
    return render(
        request=request,
        template_name="posts/details.html",
        context={"post": post, 'title': title}
    )


def author_list(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Utworzono nowego autora!"
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                form.errors['__all__']
            )

    form = AuthorForm()
    authors = Author.objects.all()
    title = 'Autorzy'
    return render(
        request=request,
        template_name="posts/author_list.html",
        context={"authors": authors, "title": title, "form": form}
    )

#@login_required
def author_details(request, id):
    author = Author.objects.get(id=id)
    title = 'Detale autora'
    return render(
        request=request,
        template_name="posts/author_details.html",
        context={"author": author, 'title': title}
    )