from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'index.html', context)


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'form.html', context)

@login_required
def likes(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect('posts:index')