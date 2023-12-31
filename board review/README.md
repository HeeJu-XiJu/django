1. `.gitignore`, `README.md` 작성

2. 프로젝트 생성
```
django-admin startproject <pjtname> .
```

3. 가상환경 설정
```python
python -m venv venv
```

4. 가상환경 활성화
```python
source venv/bin/activate
```

5. django 설치
```
pip install django
```

6. 서버 실행 확인
```python
python manage.py runserver
```

7. 앱 생성
```
django-admin startapp <appname>
```

8. 앱 등록 \
`setting.py`의 `INSTALLED_APPS` `<appname>`등록

9. 공통 base.html 작성
`setting.py` - `TEMPLATES`
```
'DIRS': [BASE_DIR / 'templates'],
```

`board`-`urls.py`
```
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
]
```

`<appname>`의 `urls.py` 생성 후
```
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
]
```

`views.py`
```
def index(request):
    return render(request, 'index.html')
```

`templates`생성 후 
`base.html`
```
<body>
    <h1>base</h1>
    {% block body %}

    {% endblock %}
</body>
```

`index.html`
```
{% extends 'base.html' %}

{% block body %}
    <h1>안녕하세요</h1>
{% endblock %}
```

10. 모델링/마이그레이션
`models.py`
```
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

- 번역본 생성
```
python manage.py makemigrations
```

- DB에 반영
```
python manage.py migrate
```

`admin.py`
```
from django.contrib import admin
from .models import Article

# Register your models here.
admin.site.register(Article)
```

- 관리자 계정 생성
```
python manage.py createsuperuser
```

11. READ(all)
`views.py`
```
from .models import Article

# Create your views here.
def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)
```

`index.html`
```
{% block body %}
    <table class="table">
        <thead>
            <tr>
                <th>#</th>
                <th>title</th>
                <th>link</th>
            </tr>
        </thead>
        <tbody>
            {% for article in articles %}
            <tr>
                <td>{{ article.id }}</td>
                <td>{{ article.title }}</td>
                <td></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
```

`<pjt> - <templates>` `base.html`
CDN 등록
Navebar 추가

12. Read(1)
`urls.py`
```
    path('<int:id>', views.detail, name='detail'),
```

`views.py`
```
def detail(request, id):
    article = Article.object.get(id=id)

    context = {
        'article': article,
    }

    return render(request, 'detail.html', context)
```

`index.html`
```
            <tr>
                <td>{{ article.id }}</td>
                <td>{{ article.title }}</td>
                <td>
                    <a href="{% url 'articles:detail' id=article.id %}">detail</a>
                </td>
            </tr>
```

13. Create
`urls.py`
```
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
```

`base.html`
```
# Nevbar
        <a class="navbar-brand" href="{% url 'articles:index' %}">Home</a>
        <a class="nav-link active" aria-current="page" href="{% url 'articles:new' %}">New</a>
```

`views.py`
```
def new(request):
    return render(request, 'new.html')


def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')

    article = Article()
    article.title = title
    article.content = content
    article.save()
    return redirect('articles:detail', id=article.id)
```

`new.html`
```
{% extends 'base.html' %}

{% block body %}
    <form action="{% url 'articles:create' %}" class="mt-4" method="POST">
        {% csrf_token %}
        <div class="mb-3">
            <label for="title" class="form-label">title</label>
            <input type="text" class="form-control" id="title" name="title">
        </div>

        <div class="mb-3">
            <label for="content" class="form-label">content</label>
            <textarea name="content" id="content" cols="30" rows="10" class="form-control"></textarea>
        </div>

        <input type="submit" class="btn btn-primary">
    </form>

{% endblock %}
```

14. Delete
`url.py`
```
    path('<int:id>/delete/', views.delete, name='delete'),
```

`detail.html`
```
<a href="{% url 'articles:delete' id=article.id %}" class="btn btn-danger">delete</a>
```

`views.py`
```
def delete(request, id):
    article = Article.objects.get(id=id)
    article.delete()

    return redirect('articles:index')
```

15. Update
`urls.py`
```
    path('<int:id>/edit/', views.edit, name='edit'),
    path('<int:id>/update/', views.update, name='update'),
```

`views.py`
```
def edit(request, id):
    article = Article.objects.get(id=id)

    context = {
        'article' : article,
    }
    
    return render(request, 'edit.html', context)


def update(request, id):
    # 새로운 정보
    title = request.POST.get('title')
    content = request.POST.get('content')

    # 기존 정보
    article = Article.objects.get(id=id)

    article.title = title
    article.content = content
    article.save()

    return redirect('articles:detail', id=article.id)
```

`detail.html`
```
            <a href="{% url 'articles:edit' id=article.id %}" class="btn btn-warning">edit</a>
```

`edit.html`
```
{% extends 'base.html' %}

{% block body %}
    <form action="{% url 'articles:update' id=article.id %}" class="mt-4" method="POST">
        {% csrf_token %}
        <div class="mb-3">
            <label for="title" class="form-label">title</label>
            <input type="text" class="form-control" id="title" name="title" value="{{article.title}}">
        </div>

        <div class="mb-3">
            <label for="content" class="form-label">content</label>
            <textarea name="content" id="content" cols="30" rows="10" class="form-control">{{article.content}}</textarea>
        </div>

        <input type="submit" class="btn btn-primary">
    </form>

{% endblock %}
```