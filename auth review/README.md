1. 프로젝트 생성
- `.gitignore`, `README.md`
- `django-admin startproject <pjtname> .`
- `python -m venv venv`
- `source venv/bin/activate`
- `pip install django`

2. 앱생성/앱등록, base.html등록
- `django-admin startapp <appname>`
- `setting.py`-`INSTALLED_APPS`-`<appname>`등록
- `base.html`생성
- `setting.py`-`'DIRS': [BASE_DIR, 'templates'],`

## accounts
3. 모델링/마이그레이션
- `models.py`
```
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```

- `settings.py`
```
AUTH_USER_MODEL = 'accounts.User'
```

- `admin.py`
```
from .models import User

admin.site.register(User)
```

- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py createsuperuser`

4. Index
- `auth urls.py`
```
from django.urls import path, include
    path('articles/', include('articles.urls')),
```

- `articles urls.py`
```
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
]
```

- `views.py`
```
def index(request):
    return render(request, 'index.html')
```

- `base.html`
```
<body>
    {% block body %}
    {% endblock %}
</body>
```

- `index.html`
```
{% extends 'base.html' %}

{% block body%}
    <h1>index</h1>
{% endblock %}
```

5. Signup
- `forms.py`
```
from .models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
```

- `auth urls.py`
```
path('accounts/', include('accounts.urls')),
```

- `accounts urls.py`
```
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
```

- `views.py`
```
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)
```

- `signup.html`
```
{% extends 'base.html' %}

{% block body %}
    <form action="" method="POST">
        {% csrf_token %}
        {{ form }}
        <input type="submit">
    </form>
{% endblock %}
```

6. Login
- `forms.py`
```
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
class CustumAuthenticationForm(AuthenticationForm):
    pass
```

- `urls.py`
```
path('login/', views.login, name='login'),
```

- `views.py`
```
def login(request):
    if request.method == 'POST':
        form = CustumAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = CustumAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)
```

- `login.html`
```
{% extends 'base.html' %}

{% block body %}
    <form action="" method="POST">
        {% csrf_token %}
        {{ form }}
        <input type="submit">
    </form>
{% endblock %}
```

7. Logout
- `urls.py`
```
    path('logout/', views.logout, name='logout'),
```

- `views.py`
```
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')
```

### articles
8. 모델링/마이그레이션
- `models.py`
```
from django.contrib.auth import get_user_model

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
```

- `admin.py`
```
from .models import Article

admin.site.register(Article)
```

- `python manage.py makemigrations`
- `python manage.py migrate`


9. Create
- `urls.py`
```
path('create/', views.create, name='create'),
```

- `forms.py`
```
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('user', )
```

- `create.html`
```
{% extends 'base.html' %}

{% block body %}
    <form action="" method="POST">
        {% csrf_token %}
        {{ form }}
    </form>
{% endblock %}
```

- `views.py`
```
from django.shortcuts import render, redirect

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'create.html', context)
```


10. Read(All)
- `views.py`
```
def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }
    return render(request, 'index.html', context)
```

- `index.html`
```
{% extends 'base.html' %}

{% block body%}
    <h1>index</h1>

    {% for article in articles %}
        {{ article.title }}
        {{ article.user }}
        <hr>
    {% endfor %}
{% endblock %}
```


11. Read(1)
- `index.html`
```
        <a href="{% url 'articles:detail' id=article.id %}">detail</a>
```

- `urls.py`
```
    path('<int:id>/', views.detail, name='detail'),
```

- `views.py`
```
def detail(request, id):
    article = Article.objects.get(id=id)
    context = {
        'article': article, 
    }
    return render(request, 'detail.html', context)
```

- `detail.html`
```
{% extends 'base.html' %}

{% block body %}
    <h3>{{ article.title }}</h3>
    <p>{{ article.content}}</p>
    <p>{{ article.user }}</p>
{% endblock %}
```


12. Delete
- `index.html`
```
<a href="{% url 'articles:delete' id=article.id %}">delete</a>
```

- `urls.py`
```
path('<int:id>/delete/', views.delete, name='delete'),
```

- `views.py`
```
def delete(request, id):
    article = Article.objects.get(id=id)
    article.delete()
    return redirect('articles:index')
```


13. Update
- `detail.html`
```
<a href="{% url 'articles:update' id=article.id %}">update</a>
```

- `urls.py`
```
path('<int:id>/update/', views.update, name='update'),
```

- `views.py`
```
def update(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('articles:detail', id=id)
    else:
        form = ArticleForm(instance=article)
    context = {
        'form': form, 
    }
    return render(request, 'create.html', context)
```

### Articles(Comment)
14. 모델링/마이그레이션
- `models.py`
```
class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
```

- `python manage.py makemigrations`
- `python manage.py migrate`


15. Create
- `form.py`
```
from .models import Article, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
```

- `urls.py`
```
    path('<int:article_id>/comments/create/', views.comment_create, name='comment_create'),
```

- `detail.html`
```
<form action="{% url 'articles:comment_create' article_id=article.id %}" method="POST">
        {% csrf_token %}
        {{ form }}
        <input type="submit">
    </form>
```

- `views.py`
```
def detail(request, id):
    form = CommentForm()
    context = {
        'article': article, 
        'form': form,
    }

from .form import ArticleForm, CommentForm

def comment_create(request, article_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)

        comment.user_id = request.user.id
        comment.article_id = article_id

        comment.save()
        return redirect('articles:detail', id=article_id)
```


16. login_required/next 인자처리
- `accounts`-`views.py`
```
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.GET.get('next')
            return redirect(next_url or 'articles:index')
```

- `views.py`
```
from django.contrib.auth.decorators import login_required

@login_required
def create(request):

@login_required
def comment_create(request, article_id):
```

- `detail.html`
```
    {% if user.is_authenticated %}
        <form action="{% url 'articles:comment_create' article_id=article.id %}" method="POST">
            {% csrf_token %}
            {{ form }}
            <input type="submit">
        </form>
    {% endif %}
```


17. Comment Read
- `detail.html`
```
<hr>
    {% for comment in article.comment_set.all %}
    <li>{{ comment.user }} : {{comment.content }}</li>
    {% endfor %}
```


18. Comment Delete
- `detail.html`
```
    <hr>
    {% for comment in article.comment_set.all %}
    <li>{{ comment.user }} : {{comment.content }}</li>
        {% if user == comment.user %}
        <a href="{% url 'articles:comment_delete' article_id=article.id id=comment.id %}">delete</a>
        {% endif %}
    {% endfor %}
```

- `urls.py`
```
path('<int:article_id>/comments/<int:id>/delete', views.comment_delete, name='comment_delete'),
```

- `views.py`
```
from .models import Article, Comment

@login_required
def comment_delete(request, article_id, id):
    comment = Comment.objects.get(id=id)
    if request.user == comment.user:
        comment.delete()
        return redirect('articles:detail', id=article_id)
```


19. User에 따른 기능 구현
- `detail.html`(update)
```
{% if user == article.user %}
    <a href="{% url 'articles:update' id=article.id %}">update</a>
    {% endif %}
```

- `index.html`(delete)
```
{% if user == article.user %}
        <a href="{% url 'articles:delete' id=article.id %}">delete</a>
        {% endif %}
```

- `views.py`
```
@login_required
def delete(request, id):
    article = Article.objects.get(id=id)
    
    if request.user == article.user:
        article.delete()
        return redirect('articles:index')

@login_required
def update(request, id):
    article = Article.objects.get(id=id)

    if request.user != article.user:
        return redirect('articles:detail', id=id)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('articles:detail', id=id)
    else:
        form = ArticleForm(instance=article)
    context = {
        'form': form, 
    }
    return render(request, 'create.html', context)
```