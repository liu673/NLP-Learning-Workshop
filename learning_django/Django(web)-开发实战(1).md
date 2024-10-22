# 1.创建应用

## 查看Django版本

```shell
python -m django --version
```

## 创建项目

```shell
django-admin startproject mysite
```

## 测试项目是否成功

```shell
python manage.py runserver
```

## 创建应用

```shell
python manage.py startapp polls
```

## 编写视图

polls/views.py

```python
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

polls/urls.py

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

同时在 `mysite/urls.py` 文件的 `urlpatterns` 列表里插入一个 `include()`， 如下：

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
```

## 检验是否正常工作

```shell
python manage.py runserver

# 用你的浏览器访问 http://localhost:8000/polls/
```



# 2.数据库配置

## 创建数据表

```shell
python manage.py migrate
```

## 创建模型

在这个投票应用`(polls)`中，需要创建两个模型：问题 `Question` 和选项 `Choice`。`Question` 模型包括问题描述和发布时间。`Choice` 模型有两个字段，选项描述和当前得票数。每个选项属于一个问题。

这些概念可以通过一个 Python 类来描述。按照下面的例子来编辑 `polls/models.py` 文件：

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

## 激活模型

为了在我们的工程中包含这个应用，我们需要在配置类 [`INSTALLED_APPS`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-INSTALLED_APPS) 中添加设置。因为 `PollsConfig` 类写在文件 `polls/apps.py` 中，所以它的点式路径是 `'polls.apps.PollsConfig'`。在文件 `mysite/settings.py` 中 [`INSTALLED_APPS`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-INSTALLED_APPS) 子项添加点式路径后，它看起来像这样：

```python
INSTALLED_APPS = [
    "polls.apps.PollsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

Django 项目会包含 `polls` 应用。接着运行下面的命令：

```shell
python manage.py makemigrations polls
```

通过运行 `makemigrations` 命令，Django 会检测你对模型文件的修改（在这种情况下，你已经取得了新的），并且把修改的部分储存为一次 *迁移*。

迁移是 Django 对于模型定义（也就是你的数据库结构）的变化的储存形式 - 它们其实也只是一些你磁盘上的文件。如果你想的话，你可以阅读一下你模型的迁移数据，它被储存在 `polls/migrations/0001_initial.py` 里。别担心，你不需要每次都阅读迁移文件，但是它们被设计成人类可读的形式，这是为了便于你手动调整 Django 的修改方式。

Django 有一个自动执行数据库迁移并同步管理你的数据库结构的命令 - 这个命令是 [`migrate`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#django-admin-migrate)，我们马上就会接触它 - 但是首先，让我们看看迁移命令会执行哪些 SQL 语句。[`sqlmigrate`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#django-admin-sqlmigrate) 命令接收一个迁移的名称，然后返回对应的 SQL：

```shell
python manage.py sqlmigrate polls 0001
```

再次运行 [`migrate`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#django-admin-migrate) 命令，在数据库里创建新定义的模型的数据表：

```shell
python manage.py migrate
```

这个 [`migrate`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#django-admin-migrate) 命令选中所有还没有执行过的迁移（Django 通过在数据库中创建一个特殊的表 `django_migrations` 来跟踪执行过哪些迁移）并应用在数据库上 - 也就是将你对模型的更改同步到数据库结构上。

迁移是非常强大的功能，它能让你在开发过程中持续的改变数据库结构而不需要重新删除和创建表 - 它专注于使数据库平滑升级而不会丢失数据。我们会在后面的教程中更加深入的学习这部分内容，现在，你只需要记住，改变模型需要这三步：

- 编辑 `models.py` 文件，改变模型。
- 运行 [`python manage.py makemigrations`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#django-admin-makemigrations) 为模型的改变生成迁移文件。
- 运行 [`python manage.py migrate`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#django-admin-migrate) 来应用数据库迁移。

数据库迁移被分解成生成和应用两个命令是为了让你能够在代码控制系统上提交迁移数据并使其能在多个应用里使用；这不仅仅会让开发更加简单，也给别的开发者和生产环境中的使用带来方便。

## 初试API

```shell
python manage.py shell
```

导入API

```shell
>>> from polls.models import Choice, Question  # Import the model classes we just wrote.

# No questions are in the system yet.
>>> Question.objects.all()
<QuerySet []>

# Create a new Question.
# Support for time zones is enabled in the default settings file, so
# Django expects a datetime with tzinfo for pub_date. Use timezone.now()
# instead of datetime.datetime.now() and it will do the right thing.
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())

# Save the object into the database. You have to call save() explicitly.
>>> q.save()

# Now it has an ID.
>>> q.id
1

# Access model field values via Python attributes.
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=datetime.timezone.utc)

# Change values by changing the attributes, then calling save().
>>> q.question_text = "What's up?"
>>> q.save()

# objects.all() displays all the questions in the database.
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>
```

`<Question: Question object (1)>` 对于我们了解这个对象的细节没什么帮助。让我们通过编辑 `Question` 模型的代码（位于 `polls/models.py` 中）来修复这个问题。给 `Question` 和 `Choice` 增加 [`__str__()`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/instances/#django.db.models.Model.__str__) 方法。

```python
from django.db import models


class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    # ...
    def __str__(self):
        return self.choice_text
```

给模型增加 [`__str__()`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/instances/#django.db.models.Model.__str__) 方法是很重要的，这不仅仅能给你在命令行里使用带来方便，Django 自动生成的 admin 里也使用这个方法来表示对象。

让我们再为此模型添加一个自定义方法：

```python
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    # ...
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```

然后再`python manage.py shell`

```shell
>>> from polls.models import Choice, Question

# Make sure our __str__() addition worked.
>>> Question.objects.all()
<QuerySet [<Question: What's up?>]>

# Django provides a rich database lookup API that's entirely driven by
# keyword arguments.
>>> Question.objects.filter(id=1)
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith="What")
<QuerySet [<Question: What's up?>]>

# Get the question that was published this year.
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
<Question: What's up?>

# Request an ID that doesn't exist, this will raise an exception.
>>> Question.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: Question matching query does not exist.

# Lookup by a primary key is the most common case, so Django provides a
# shortcut for primary-key exact lookups.
# The following is identical to Question.objects.get(id=1).
>>> Question.objects.get(pk=1)
<Question: What's up?>

# Make sure our custom method worked.
>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()
True

# Give the Question a couple of Choices. The create call constructs a new
# Choice object, does the INSERT statement, adds the choice to the set
# of available choices and returns the new Choice object. Django creates
# a set to hold the "other side" of a ForeignKey relation
# (e.g. a question's choice) which can be accessed via the API.
>>> q = Question.objects.get(pk=1)

# Display any choices from the related object set -- none so far.
>>> q.choice_set.all()
<QuerySet []>

# Create three choices.
>>> q.choice_set.create(choice_text="Not much", votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text="The sky", votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text="Just hacking again", votes=0)

# Choice objects have API access to their related Question objects.
>>> c.question
<Question: What's up?>

# And vice versa: Question objects get access to Choice objects.
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
3

# The API automatically follows relationships as far as you need.
# Use double underscores to separate relationships.
# This works as many levels deep as you want; there's no limit.
# Find all Choices for any question whose pub_date is in this year
# (reusing the 'current_year' variable we created above).
>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

# Let's delete one of the choices. Use delete() for that.
>>> c = q.choice_set.filter(choice_text__startswith="Just hacking")
>>> c.delete()
```



## Django管理页面

创建一个管理员账号

```shell
python manage.py createsuperuser

# 使用的用户名
Username: admin

# 邮件地址
Email address: admin@example.com

# 输入密码
Password: **********
Password (again): *********
Superuser created successfully.
```

启动开发服务器

```shell
python manage.py runserver
```

进入管理站点

```
点击的url+/admin
```

向管理页面中加入投票应用

在polls/admin.py文件编辑如下

```python
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

# 3.视图

在 Django 中，网页和其他内容都是从视图派生而来。每一个视图表现为一个 Python 函数（或者说方法，如果是在基于类的视图里的话）。Django 将会根据用户请求的 URL 来选择使用哪个视图（更准确的说，是根据 URL 中域名之后的部分）。

URL 样式是 URL 的一般形式 - 例如：`/newsarchive/<year>/<month>/`。

为了将 URL 和视图关联起来，Django 使用了 'URLconfs' 来配置。URLconf 将 URL 模式映射到视图。



## 编写更多视图

polls/views.py里添加更多视图

```python
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

把这些新视图添加进 `polls.urls` 模块里，只要添加几个 `url()` 函数调用就行：

```python
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

## 真正有用的视图

每个视图必须要做的只有两件事：返回一个包含被请求页面内容的 [`HttpResponse`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpResponse) 对象，或者抛出一个异常，比如 [`Http404`](https://docs.djangoproject.com/zh-hans/4.2/topics/http/views/#django.http.Http404) 。至于你还想干些什么，随便你。

你的视图可以从数据库里读取记录，可以使用一个模板引擎（比如 Django 自带的，或者其他第三方的），可以生成一个 PDF 文件，可以输出一个 XML，创建一个 ZIP 文件，你可以做任何你想做的事，使用任何你想用的 Python 库。

Django 只要求返回的是一个 [`HttpResponse`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpResponse) ，或者抛出一个异常。

试试在视图里使用它。我们在 `index()` 函数里插入了一些新内容，让它能展示数据库里以发布日期排序的最近 5 个投票问题，以空格分割：

```python
from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)


# Leave the rest of the views (detail, results, vote) unchanged
```

这里有个问题：页面的设计写死在视图函数的代码里的。如果你想改变页面的样子，你需要编辑 Python 代码。所以让我们使用 Django 的模板系统，只要创建一个视图，就可以将页面的设计从代码中分离出来。

首先，在你的 `polls` 目录里创建一个 `templates` 目录。Django 将会在这个目录里查找模板文件。

你项目的 [`TEMPLATES`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-TEMPLATES) 配置项描述了 Django 如何载入和渲染模板。默认的设置文件设置了 `DjangoTemplates` 后端，并将 [`APP_DIRS`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-TEMPLATES-APP_DIRS) 设置成了 True。这一选项将会让 `DjangoTemplates` 在每个 [`INSTALLED_APPS`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-INSTALLED_APPS) 文件夹中寻找 "templates" 子目录。这就是为什么尽管我们没有像在第二部分中那样修改 DIRS 设置，Django 也能正确找到 polls 的模板位置的原因。

在你刚刚创建的 `templates` 目录里，再创建一个目录 `polls`，然后在其中新建一个文件 `index.html` 。换句话说，你的模板文件的路径应该是 `polls/templates/polls/index.html` 。因为``app_directories`` 模板加载器是通过上述描述的方法运行的，所以 Django 可以引用到 `polls/index.html` 这一模板了。

将下面代码加入创建的模版文件中

```html
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

然后，让我们更新一下 `polls/views.py` 里的 `index` 视图来使用模板：

```python
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))

# 上述代码的作用是，载入 polls/index.html 模板文件，并且向它传递一个上下文(context)。这个上下文是一个字典，它将模板内的变量映射为 Python 对象。
# 用你的浏览器访问 "/polls/" ，你将会看见一个无序列表，列出了我们在 教程第 2 部分 中添加的 “What's up” 投票问题，链接指向这个投票的详情页
```



### 快捷函数：render()

「载入模板，填充上下文，再返回由它生成的 [`HttpResponse`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpResponse) 对象」是一个非常常用的操作流程。于是 Django 提供了一个快捷函数，我们用它来重写 `index()` 视图：

```python
from django.shortcuts import render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

# 注意到，我们不再需要导入 loader 和 HttpResponse 。不过如果你还有其他函数（比如说 detail, results, 和 vote ）需要用到它的话，就需要保持 HttpResponse 的导入。
```

### 抛出404错误

我们来处理投票详情视图——它会显示指定投票的问题标题。下面是这个视图的代码：

```python
from django.http import Http404
from django.shortcuts import render

from .models import Question


# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})
```

这里有个新原则。如果指定问题 ID 所对应的问题不存在，这个视图就会抛出一个 [`Http404`](https://docs.djangoproject.com/zh-hans/4.2/topics/http/views/#django.http.Http404) 异常。

我们稍后再讨论你需要在 `polls/detail.html` 里输入什么，但是如果你想试试上面这段代码是否正常工作的话，你可以暂时把下面这段输进去：

```html
{{ question }}
```

### 快捷函数:get_object_or_404()

尝试用 [`get()`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/querysets/#django.db.models.query.QuerySet.get) 函数获取一个对象，如果不存在就抛出 [`Http404`](https://docs.djangoproject.com/zh-hans/4.2/topics/http/views/#django.http.Http404) 错误也是一个普遍的流程。Django 也提供了一个快捷函数，下面是修改后的详情 `detail()` 视图代码：

```python
from django.shortcuts import get_object_or_404, render

from .models import Question


# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
```

使用模版系统

回过头去看看我们的 `detail()` 视图。它向模板传递了上下文变量 `question` 。下面是 `polls/detail.html` 模板里正式的代码：

```html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```

模板系统统一使用点符号来访问变量的属性。在示例 `{{ question.question_text }}` 中，首先 Django 尝试对 `question` 对象使用字典查找（也就是使用 obj.get(str) 操作），如果失败了就尝试属性查找（也就是 obj.str 操作），结果是成功了。如果这一操作也失败的话，将会尝试列表查找（也就是 obj[int] 操作）。

在 [`{% for %}`](https://docs.djangoproject.com/zh-hans/4.2/ref/templates/builtins/#std-templatetag-for) 循环中发生的函数调用：`question.choice_set.all` 被解释为 Python 代码 `question.choice_set.all()` ，将会返回一个可迭代的 `Choice` 对象，这一对象可以在 [`{% for %}`](https://docs.djangoproject.com/zh-hans/4.2/ref/templates/builtins/#std-templatetag-for) 标签内部使用。



### 去除模版中的硬编码URL

我们在 `polls/index.html` 里编写投票链接时，链接是硬编码的：

```html
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
```

问题在于，硬编码和强耦合的链接，对于一个包含很多应用的项目来说，修改起来是十分困难的。然而，因为你在 `polls.urls` 的 `url()` 函数中通过 name 参数为 URL 定义了名字，你可以使用 `{% url %}` 标签代替它：

```html
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

这个标签的工作方式是在 `polls.urls` 模块的 URL 定义中寻具有指定名字的条目。你可以回忆一下，具有名字 'detail' 的 URL 是在如下语句中定义的：

```python
...
# the 'name' value as called by the {% url %} template tag
path("<int:question_id>/", views.detail, name="detail"),
...
```

如果你想改变投票详情视图的 URL，比如想改成 `polls/specifics/12/` ，你不用在模板里修改任何东西（包括其它模板），只要在 `polls/urls.py` 里稍微修改一下就行：

```python
...
# added the word 'specifics'
path("specifics/<int:question_id>/", views.detail, name="detail"),
..
```

### 为URL名称添加命名空间

教程项目只有一个应用，`polls` 。在一个真实的 Django 项目中，可能会有五个，十个，二十个，甚至更多应用。Django 如何分辨重名的 URL 呢？举个例子，`polls` 应用有 `detail` 视图，可能另一个博客应用也有同名的视图。Django 如何知道 `{% url %}` 标签到底对应哪一个应用的 URL 呢？

答案是：在根 URLconf 中添加命名空间。在 `polls/urls.py` 文件中稍作修改，加上 `app_name` 设置命名空间

```python
from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

编辑 `polls/index.html` 文件，从：

```html
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

修改为指向具有命名空间的详细视图：

```html
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```

# 4.表单处理

## 编写一个简单的表单

在上一个教程中编写的投票详细页面的模板 ("polls/detail.html") ，让它包含一个 HTML `<form>` 元素：

```html
<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
<fieldset>
    <legend><h1>{{ question.question_text }}</h1></legend>
    {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    {% endfor %}
</fieldset>
<input type="submit" value="Vote">
</form>
```

简要说明：

- 上面的模板在 Question 的每个 Choice 前添加一个单选按钮。 每个单选按钮的 `value` 属性是对应的各个 Choice 的 ID。每个单选按钮的 `name` 是 `"choice"` 。这意味着，当有人选择一个单选按钮并提交表单提交时，它将发送一个 POST 数据 `choice=#` ，其中# 为选择的 Choice 的 ID。这是 HTML 表单的基本概念。
- 我们将表单的 `action` 设置为 `{% url 'polls:vote' question.id %}`，并设置 `method="post"`。使用 `method="post"` （而不是 `method="get"` ）是非常重要的，因为提交这个表单的行为将改变服务器端的数据。当你创建一个改变服务器端数据的表单时，使用 `method="post"`。这不是 Django 的特定技巧；这是优秀的网站开发技巧。
- `forloop.counter` 指示 [`for`](https://docs.djangoproject.com/zh-hans/4.2/ref/templates/builtins/#std-templatetag-for) 标签已经循环多少次。
- 由于我们创建一个 POST 表单（它具有修改数据的作用），所以我们需要小心跨站点请求伪造。 谢天谢地，你不必太过担心，因为 Django 自带了一个非常有用的防御系统。 简而言之，所有针对内部 URL 的 POST 表单都应该使用 [`{% csrf_token %}`](https://docs.djangoproject.com/zh-hans/4.2/ref/templates/builtins/#std-templatetag-csrf_token) 模板标签。

现在，让我们来创建一个 Django 视图来处理提交的数据。记住，在 [教程第 3 部分](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial03/) 中，我们为投票应用创建了一个 URLconf ，包含这一行：

`polls/urls.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial04/#id2)

```python
path("<int:question_id>/vote/", views.vote, name="vote"),
```

我们还创建了一个 `vote()` 函数的虚拟实现。让我们来创建一个真实的版本。 将下面的代码添加到 `polls/views.py` ：

```python
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


# ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
```

以上代码中有些内容还未在本教程中提到过：

- [`request.POST`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpRequest.POST) 是一个类字典对象，让你可以通过关键字的名字获取提交的数据。 这个例子中， `request.POST['choice']` 以字符串形式返回选择的 Choice 的 ID。 [`request.POST`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpRequest.POST) 的值永远是字符串。

  注意，Django 还以同样的方式提供 [`request.GET`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpRequest.GET) 用于访问 GET 数据 —— 但我们在代码中显式地使用 [`request.POST`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpRequest.POST) ，以保证数据只能通过 POST 调用改动。

- 如果在 `request.POST['choice']` 数据中没有提供 `choice` ， POST 将引发一个 [`KeyError`](https://docs.python.org/3/library/exceptions.html#KeyError) 。上面的代码检查 [`KeyError`](https://docs.python.org/3/library/exceptions.html#KeyError) ，如果没有给出 `choice` 将重新显示 Question 表单和一个错误信息。

- 在增加 Choice 的得票数之后，代码返回一个 [`HttpResponseRedirect`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpResponseRedirect) 而不是常用的 [`HttpResponse`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpResponse) 、 [`HttpResponseRedirect`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpResponseRedirect) 只接收一个参数：用户将要被重定向的 URL（请继续看下去，我们将会解释如何构造这个例子中的 URL）。

  正如上面的 Python 注释指出的，在成功处理 POST 数据后，你应该总是返回一个 [`HttpResponseRedirect`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpResponseRedirect)。这不是 Django 的特殊要求，这是那些优秀网站在开发实践中形成的共识。

- 在这个例子中，我们在 [`HttpResponseRedirect`](https://docs.djangoproject.com/zh-hans/4.2/ref/request-response/#django.http.HttpResponseRedirect) 的构造函数中使用 `reverse()` 函数。这个函数避免了我们在视图函数中硬编码 URL。它需要我们给出我们想要跳转的视图的名字和该视图所对应的 URL 模式中需要给该视图提供的参数。 在本例中，使用在 [教程第 3 部分](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial03/) 中设定的 URLconf， `reverse()` 调用将返回一个这样的字符串：

  ```
  "/polls/3/results/"
  ```

  其中 `3` 是 `question.id` 的值。重定向的 URL 将调用 `'results'` 视图来显示最终的页面。

当有人对 Question 进行投票后， `vote()` 视图将请求重定向到 Question 的结果界面。让我们来编写这个视图：

`polls/views.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial04/#id4)

```python
from django.shortcuts import get_object_or_404, render


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
```

这和 [教程第 3 部分](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial03/) 中的 `detail()` 视图几乎一模一样。唯一的不同是模板的名字。 我们将在稍后解决这个冗余问题。

现在，创建一个 `polls/results.html` 模板：

现在，创建一个 `polls/results.html` 模板：

`polls/templates/polls/results.html`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial04/#id5)

```html
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```

现在，在你的浏览器中访问 `/polls/1/` 然后为 Question 投票。你应该看到一个投票结果页面，并且在你每次投票之后都会更新。 如果你提交时没有选择任何 Choice，你应该看到错误信息。

## 使用通用视图：代码还是少点好

`detail()` （在 [教程第 3 部分](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial03/) 中）和 `results()` 视图都很精简 —— 并且，像上面提到的那样，存在冗余问题。用来显示一个投票列表的 `index()` 视图（也在 [教程第 3 部分](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial03/) 中）和它们类似。

这些视图反映基本的网络开发中的一个常见情况：根据 URL 中的参数从数据库中获取数据、载入模板文件然后返回渲染后的模板。 由于这种情况特别常见，Django 提供一种快捷方式，叫做 “通用视图” 系统。

Generic views abstract common patterns to the point where you don't even need to write Python code to write an app. For example, the [`ListView`](https://docs.djangoproject.com/zh-hans/4.2/ref/class-based-views/generic-display/#django.views.generic.list.ListView) and [`DetailView`](https://docs.djangoproject.com/zh-hans/4.2/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView) generic views abstract the concepts of "display a list of objects" and "display a detail page for a particular type of object" respectively.

让我们将我们的投票应用转换成使用通用视图系统，这样我们可以删除许多我们的代码。我们仅仅需要做以下几步来完成转换，我们将：

1. 转换 URLconf。
2. 删除一些旧的、不再需要的视图。
3. 基于 Django 的通用视图引入新的视图。

## 改良URLconf

首先，打开 `polls/urls.py` 这个 URLconf 并将它修改成：

`polls/urls.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial04/#id6)

```python
from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

请注意，第二个和第三个模式的路径字符串中匹配模式的名称已从 `<question_id>` 更改为 `<pk>` 。这是必要的，因为我们将使用 `DetailView` 通用视图来替换我们的 `detail()` 和 `results()` 视图，并且它期望从 URL 捕获的主键值被调用 `"pk"` 。

## 改良视图

下一步，我们将删除旧的 `index`, `detail`, 和 `results` 视图，并用 Django 的通用视图代替。打开 `polls/views.py` 文件，并将它修改成：

```python
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    ...  # same as above, no changes needed.
```

每个通用视图都需要知道它将对哪个模型执行操作。这是使用 `model` 属性（在本例中为 `model = Question` for `DetailView` 和 `ResultsView` ）或通过定义 `get_queryset()` 方法（如 所示） `IndexView` 提供的。

默认情况下，通用视图 [`DetailView`](https://docs.djangoproject.com/zh-hans/4.2/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView) 使用一个叫做 `<app name>/<model name>_detail.html` 的模板。在我们的例子中，它将使用 `"polls/question_detail.html"` 模板。`template_name` 属性是用来告诉 Django 使用一个指定的模板名字，而不是自动生成的默认名字。 我们也为 `results` 列表视图指定了 `template_name` —— 这确保 results 视图和 detail 视图在渲染时具有不同的外观，即使它们在后台都是同一个 [`DetailView`](https://docs.djangoproject.com/zh-hans/4.2/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView) 。

类似地，[`ListView`](https://docs.djangoproject.com/zh-hans/4.2/ref/class-based-views/generic-display/#django.views.generic.list.ListView) 使用一个叫做 `<app name>/<model name>_list.html` 的默认模板；我们使用 `template_name` 来告诉 [`ListView`](https://docs.djangoproject.com/zh-hans/4.2/ref/class-based-views/generic-display/#django.views.generic.list.ListView) 使用我们创建的已经存在的 `"polls/index.html"` 模板。

在之前的教程中，提供模板文件时都带有一个包含 `question` 和 `latest_question_list` 变量的 context。对于 `DetailView` ， `question` 变量会自动提供—— 因为我们使用 Django 的模型（Question）， Django 能够为 context 变量决定一个合适的名字。然而对于 ListView， 自动生成的 context 变量是 `question_list`。为了覆盖这个行为，我们提供 `context_object_name` 属性，表示我们想使用 `latest_question_list`。作为一种替换方案，你可以改变你的模板来匹配新的 context 变量 —— 这是一种更便捷的方法，告诉 Django 使用你想使用的变量名。

启动服务器，使用一下基于通用视图的新投票应用。



# 5.自动测试

## 写第一个测试

### 首先得有个BUG

幸运的是，我们的 `polls` 应用现在就有一个小 bug 需要被修复：我们的要求是如果 Question 是在一天之内发布的， `Question.was_published_recently()` 方法将会返回 `True` ，然而现在这个方法在 `Question` 的 `pub_date` 字段比当前时间还晚时也会返回 True（这是个 Bug）。

用djadmin:[`](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial05/#id1)shell`命令确认一下这个方法的日期bug

```shell
python manage.py shell

>>> import datetime
>>> from django.utils import timezone
>>> from polls.models import Question
>>> # create a Question instance with pub_date 30 days in the future
>>> future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
>>> # was it published recently?
>>> future_question.was_published_recently()
True
```

因为将来发生的肯定不是最近发生的，所以代码明显是错误的

### 创建一个测试来暴露这个BUG

我们刚刚在 [`shell`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#django-admin-shell) 里做的测试也就是自动化测试应该做的工作。所以我们来把它改写成自动化的吧。

按照惯例，Django 应用的测试应该写在应用的 `tests.py` 文件里。测试系统会自动的在所有文件里寻找并执行以 `test` 开头的测试函数。

将下面的代码写入 `polls` 应用里的 `tests.py` 文件内：

```python
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
   
# 我们创建了一个 django.test.TestCase 的子类，并添加了一个方法，此方法创建一个 pub_date 时未来某天的 Question 实例。然后检查它的 was_published_recently() 方法的返回值——它 应该 是 False。
```

### 运行测试

```shell
$ python manage.py test polls

```

发生了什么呢？以下是自动化测试的运行过程：

- `python manage.py test polls` 将会寻找 `polls` 应用里的测试代码
- 它找到了 [`django.test.TestCase`](https://docs.djangoproject.com/zh-hans/4.2/topics/testing/tools/#django.test.TestCase) 的一个子类
- 它创建一个特殊的数据库供测试使用
- 它在类中寻找测试方法——以 `test` 开头的方法。
- 在 `test_was_published_recently_with_future_question` 方法中，它创建了一个 `pub_date` 值为 30 天后的 `Question` 实例。
- 接着使用 `assertls()` 方法，发现 `was_published_recently()` 返回了 `True`，而我们期望它返回 `False`。

测试系统通知我们哪些测试样例失败了，和造成测试失败的代码所在的行号。

### 修复这个BUG

我们早已知道，当 `pub_date` 为未来某天时， `Question.was_published_recently()` 应该返回 `False`。我们修改 `models.py` 里的方法，让它只在日期是过去式的时候才返回 `True`：

`polls/models.py`

```python
def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now
```

再次运行测试代码,，发现BUG已经被修复

```shell
$ python manage.py test polls
```

### 更全面的测试

我们已经搞定一小部分了，现在可以考虑全面的测试 `was_published_recently()` 这个方法以确定它的安全性，然后就可以把这个方法稳定下来了。事实上，在修复一个 bug 时不小心引入另一个 bug 会是非常令人尴尬的。

我们在上次写的类里再增加两个测试，来更全面的测试这个方法：

```python
def test_was_published_recently_with_old_question(self):
    """
    was_published_recently() returns False for questions whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(), False)


def test_was_published_recently_with_recent_question(self):
    """
    was_published_recently() returns True for questions whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)
```

现在，我们有三个测试来确保 `Question.was_published_recently()` 方法对于过去，最近，和将来的三种情况都返回正确的值。

再次申明，尽管 `polls` 现在是个小型的应用，但是无论它以后变得到多么复杂，无论他和其他代码如何交互，我们可以在一定程度上保证我们为之编写测试的方法将按照预期的方式运行。

## 测试视图

我们的投票应用对所有问题都一视同仁：它将会发布所有的问题，也包括那些 `pub_date` 字段值是未来的问题。我们应该改善这一点。如果 `pub_date` 设置为未来某天，这应该被解释为这个问题将在所填写的时间点才被发布，而在之前是不可见的。

### 针对视图的测试

为了修复上述 bug ，我们这次先编写测试，然后再去改代码。事实上，这是一个「测试驱动」开发模式的实例，但其实这两者的顺序不太重要。

在我们的第一个测试中，我们关注代码的内部行为。我们通过模拟用户使用浏览器访问被测试的应用来检查代码行为是否符合预期。

在我们动手之前，先看看需要用到的工具们。

### Django测试工具之Client

Django 提供了一个供测试使用的 [`Client`](https://docs.djangoproject.com/zh-hans/4.2/topics/testing/tools/#django.test.Client) 来模拟用户和视图层代码的交互。我们能在 `tests.py` 甚至是 [`shell`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#django-admin-shell) 中使用它。

我们依照惯例从 [`shell`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#django-admin-shell) 开始，首先我们要做一些在 `tests.py` 里不是必须的准备工作。第一步是在 [`shell`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#django-admin-shell) 中配置测试环境:

```shell
$ python manage.py shell

>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
```

[`setup_test_environment()`](https://docs.djangoproject.com/zh-hans/4.2/topics/testing/advanced/#django.test.utils.setup_test_environment) 安装了一个模板渲染器，这将使我们能够检查响应上的一些额外属性，如 `response.context`，否则将无法使用此功能。请注意，这个方法 *不会* 建立一个测试数据库，所以下面的内容将针对现有的数据库运行，输出结果可能略有不同，这取决于你已经创建了哪些问题。如果你在 `settings.py` 中的 `TIME_ZONE` 不正确，你可能会得到意外的结果。如果你不记得之前的配置，请在继续之前检查。

接下来，我们需要导入Client类（稍后 `tests.py` 我们将使用该类，该 `django.test.TestCase` 类自带客户端，因此不需要）：

```
>>> from django.test import Client
>>> # create an instance of the client for our use
>>> client = Client()
```

准备好后，我们可以要求Client为我们做一些工作：

```shell
>>> # get a response from '/'
>>> response = client.get("/")
Not Found: /
>>> # we should expect a 404 from that address; if you instead see an
>>> # "Invalid HTTP_HOST header" error and a 400 response, you probably
>>> # omitted the setup_test_environment() call described earlier.
>>> response.status_code
404
>>> # on the other hand we should expect to find something at '/polls/'
>>> # we'll use 'reverse()' rather than a hardcoded URL
>>> from django.urls import reverse
>>> response = client.get(reverse("polls:index"))
>>> response.status_code
200
>>> response.content
b'\n    <ul>\n    \n        <li><a href="/polls/1/">What&#x27;s up?</a></li>\n    \n    </ul>\n\n'
>>> response.context["latest_question_list"]
<QuerySet [<Question: What's up?>]>
```

### 改善视图代码

现在的投票列表会显示将来的投票（ `pub_date` 值是未来的某天)。我们来修复这个问题。

基于 [`ListView`](https://docs.djangoproject.com/zh-hans/4.2/ref/class-based-views/generic-display/#django.views.generic.list.ListView) 的视图类：

`polls/views.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial05/#id4)

```python
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
```

我们需要改进 `get_queryset()` 方法，让他它能通过将 Question 的 pub_data 属性与 `timezone.now()` 相比较来判断是否应该显示此 Question。首先我们需要一行 import 语句：

`polls/views.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial05/#id5)

```python
from django.utils import timezone
```

然后我们把 `get_queryset` 方法改写成下面这样：

```python
def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5
    ]
    
    
# Question.objects.filter(pub_date__lte=timezone.now()) 返回一个 Question 包含小于或等于 - 的 QuerySet，即 pub_date 早于或等于 - timezone.now 的 QuerySet。
```

### 测试新视图

启动服务器、在浏览器中载入站点、创建一些发布时间在过去和将来的 `Questions` ，然后检验只有已经发布的 `Questions` 会展示出来，现在你可以对自己感到满意了。*你不想每次修改可能与这相关的代码时都重复这样做* —— 所以让我们基于以上 [`shell`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#django-admin-shell) 会话中的内容，再编写一个测试。

将下面的代码添加到 `polls/tests.py` ：

```python
from django.urls import reverse
```

然后我们写一个公用的快捷函数用于创建投票问题，再为视图创建一个测试类：

```python
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
```

让我们更详细地看下以上这些内容。

首先是一个快捷函数 `create_question`，它封装了创建投票的流程，减少了重复代码。

`test_no_questions` 不会创建任何问题，但会检查消息：“没有可用的投票”，并验证该 `latest_question_list` 消息是否为空。请注意，该 `django.test.TestCase` 类提供了一些额外的断言方法。在这些示例中，我们使用 `assertContains()` 和 `assertQuerySetEqual()` 。

在 `test_past_question` 方法中，我们创建了一个投票并检查它是否出现在列表中。

在 `test_future_question` 中，我们创建 `pub_date` 在未来某天的投票。数据库会在每次调用测试方法前被重置，所以第一个投票已经没了，所以主页中应该没有任何投票。

剩下的那些也都差不多。实际上，测试就是假装一些管理员的输入，然后通过用户端的表现是否符合预期来判断新加入的改变是否破坏了原有的系统状态。

### 测试DetailView

我们的工作似乎已经很完美了？不，还有一个问题：就算在发布日期时未来的那些投票不会在目录页 *index* 里出现，但是如果用户知道或者猜到正确的 URL ，还是可以访问到它们。所以我们得在 `DetailView` 里增加一些约束：

`polls/views.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial05/#id9)

```python
class DetailView(generic.DetailView):
    ...

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
```

然后，我们应该增加一些测试来检验 `pub_date` 在过去的 `Question` 能够被显示出来，而 `pub_date` 在未来的则不可以：

`polls/tests.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial05/#id10)

```python
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
```

## 更多的测试思路[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial05/#ideas-for-more-tests)

我们应该给 `ResultsView` 也增加一个类似的 `get_queryset` 方法，并且为它创建测试。这和我们之前干的差不多，事实上，基本就是重复一遍。

我们还可以从各个方面改进投票应用，但是测试会一直伴随我们。比方说，在目录页上显示一个没有选项 `Choices` 的投票问题就没什么意义。我们可以检查并排除这样的投票题。测试可以创建一个没有选项的投票，然后检查它是否被显示在目录上。当然也要创建一个有选项的投票，然后确认它确实被显示了。

恩，也许你想让管理员能在目录上看见未被发布的那些投票，但是普通用户看不到。不管怎么说，如果你想要增加一个新功能，那么同时一定要为它编写测试。不过你是先写代码还是先写测试那就随你了。

在未来的某个时刻，你一定会去查看测试代码，然后开始怀疑：「这么多的测试不会使代码越来越复杂吗？」。别着急，我们马上就会谈到这一点。

## 当需要测试的时候，测试用例越多越好[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial05/#when-testing-more-is-better)

貌似我们的测试多的快要失去控制了。按照这样发展下去，测试代码就要变得比应用的实际代码还要多了。而且测试代码大多都是重复且不优雅的，特别是在和业务代码比起来的时候，这种感觉更加明显。

**但是这没关系！** 就让测试代码继续肆意增长吧。大部分情况下，你写完一个测试之后就可以忘掉它了。在你继续开发的过程中，它会一直默默无闻地为你做贡献的。

但有时测试也需要更新。想象一下如果我们修改了视图，只显示有选项的那些投票，那么只前写的很多测试就都会失败。*但这也明确地告诉了我们哪些测试需要被更新*，所以测试也会测试自己。

最坏的情况是，当你继续开发的时候，发现之前的一些测试现在看来是多余的。但是这也不是什么问题，多做些测试也 *不错*。

如果你对测试有个整体规划，那么它们就几乎不会变得混乱。下面有几条好的建议：

- 对于每个模型和视图都建立单独的 `TestClass`
- 每个测试方法只测试一个功能
- 给每个测试方法起个能描述其功能的名字

## 深入代码测试

在Django文档中查看测试用例

# 6.静态文件

## 自定义应用的界面和风格

`django.contrib.staticfiles` 存在的意义：它将各个应用的静态文件（和一些你指明的目录里的文件）统一收集起来，这样一来，在生产环境中，这些文件就会集中在一个便于分发的地方

首先，在你的 `polls` 目录下创建一个名为 `static` 的目录。Django 将在该目录下查找静态文件，这种方式和 Diango 在 `polls/templates/` 目录下查找 template 的方式类似。

Django 的 [`STATICFILES_FINDERS`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-STATICFILES_FINDERS) 设置包含了一系列的查找器，它们知道去哪里找到 static 文件。`AppDirectoriesFinder` 是默认查找器中的一个，它会在每个 [`INSTALLED_APPS`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-INSTALLED_APPS) 中指定的应用的子文件中寻找名称为 `static` 的特定文件夹，就像我们在 `polls` 中刚创建的那个一样。管理后台采用相同的目录结构管理它的静态文件。

在你刚创建的 `static` 文件夹中创建一个名为 `polls` 的文件夹，再在 `polls` 文件夹中创建一个名为 `style.css` 的文件。换句话说，你的样式表路径应是 `polls/static/polls/style.css`。因为 `AppDirectoriesFinder` 的存在，你可以在 Django 中以 `polls/style.css` 的形式引用此文件，类似你引用模板路径的方式。

将以下代码放入样式表(`polls/static/polls/style.css`)：

```css
li a {
    color: green;
}
```

下一步，在 `polls/templates/polls/index.html` 的文件头添加以下内容：

`polls/templates/polls/index.html`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial06/#id2)

```
{% load static %}

<link rel="stylesheet" href="{% static 'polls/style.css' %}">
```

`{% static %}` 模板标签会生成静态文件的绝对路径。

这就是你开发所需要做的所有事情了。

启动服务：

```shell
$ python manage.py runsever
```

## 添加一个背景图

接下来，我们将为图像创建一个子目录。 在 `polls/static/polls/` 目录中创建 `images` 子目录。 在此目录中，添加您想用作背景的任何图像文件。 出于本教程的目的，我们使用了一个名为“background.png”的文件，它的完整路径为“polls/static/polls/images/background.png”。

然后，在样式表中添加对图像的引用（`polls/static/polls/style.css`）：

`polls/static/polls/style.css`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial06/#id3)

```css
body {
    background: white url("images/background.png") no-repeat;
}
```

浏览器重载 `http://localhost:8000/polls/`，你将在屏幕的左上角见到这张背景图。

# 7.自动生成后台

## 自定义后台表单

通过 `admin.site.register(Question)` 注册 `Question` 模型，Django 能够构建一个默认的表单用于展示。通常来说，你期望能自定义表单的外观和工作方式。你可以在注册模型时将这些设置告诉 Django。

让我们通过重排列表单上的字段来看看它是怎么工作的。用以下内容替换 `admin.site.register(Question)`：

```python
from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]


admin.site.register(Question, QuestionAdmin)
```

你需要遵循以下流程——创建一个模型后台类，接着将其作为第二个参数传给 `admin.site.register()` ——在你需要修改模型的后台管理选项时这么做。

以上修改使得 "Publication date" 字段显示在 "Question" 字段之前：

说到拥有数十个字段的表单，你可能更期望将表单分为几个字段集：

```python
from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]


admin.site.register(Question, QuestionAdmin)
```

[`fieldsets`](https://docs.djangoproject.com/zh-hans/4.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets) 元组中的第一个元素是字段集的标题。

## 添加关联的对象

好了，现在我们有了投票的后台页。不过，一个 `Question` 有多个 `Choice`，但后台页却没有显示多个选项。

好了。

有两个方法可以解决这个问题。第一个就是仿照我们向后台注册 `Question` 一样注册 `Choice` ：

```python
from django.contrib import admin

from .models import Choice, Question

# ...
admin.site.register(Choice)
```

在这个表单中，"Question" 字段是一个包含数据库中所有投票的选择框。Django 知道要将 [`ForeignKey`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#django.db.models.ForeignKey) 在后台中以选择框 `<select>` 的形式展示。此时，我们只有一个投票。

还请注意“问题”旁边的“添加另一个问题”链接。每个与另一个具有`ForeignKey``关系的对象都可以免费获得此链接。当你点击“添加另一个问题”时，你会看到一个带有“添加问题”表单的弹出窗口。如果你在该窗口中添加问题并点击“保存”，Django会将问题保存到数据库中，并将其动态添加为你正在查看的“添加选项”表单上的选定选项。

不过，这是一种很低效地添加“选项”的方法。更好的办法是在你创建“投票”对象时直接添加好几个选项。让我们实现它。

移除调用 `register()` 注册 `Choice` 模型的代码。随后，像这样修改 `Question` 的注册代码：

```python
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
```

它看起来像这样：有三个关联的选项插槽——由 `extra` 定义，且每次你返回任意已创建的对象的“修改”页面时，你会见到三个新的插槽。

在三个插槽的末端，你会看到一个“添加新选项”的按钮。如果你单击它，一个新的插槽会被添加。如果你想移除已有的插槽，可以点击插槽右上角的X。

不过，仍然有点小问题。它占据了大量的屏幕区域来显示所有关联的 `Choice` 对象的字段。对于这个问题，Django 提供了一种表格式的单行显示关联对象的方法。要使用它，只需按如下形式修改 `ChoiceInline` 申明：

`polls/admin.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial07/#id5)

```python
class ChoiceInline(admin.TabularInline):
    ...
```

通过 `TabularInline` （替代 `StackedInline` ），关联对象以一种表格式的方式展示，显得更加紧凑：

## 自定义后台更改列表

现在投票的后台页看起来很不错，让我们对“更改列表”页面进行一些调整——改成一个能展示系统中所有投票的页面。

默认情况下，Django 显示每个对象的 `str()` 返回的值。但有时如果我们能够显示单个字段，它会更有帮助。为此，使用 [`list_display`](https://docs.djangoproject.com/zh-hans/4.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) 后台选项，它是一个包含要显示的字段名的元组，在更改列表页中以列的形式展示这个对象：

`polls/admin.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial07/#id6)

```python
class QuestionAdmin(admin.ModelAdmin):
    # ...
    list_display = ["question_text", "pub_date"]
```

另外，让我们把 [教程第 2 部分](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial02/) 中的 `was_published_recently()` 方法也加上：

`polls/admin.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial07/#id7)

```python
class QuestionAdmin(admin.ModelAdmin):
    # ...
    list_display = ["question_text", "pub_date", "was_published_recently"]
```

你可以点击列标题来对这些行进行排序——除了 `was_published_recently` 这个列，因为没有实现排序方法。顺便看下这个列的标题 `was_published_recently`，默认就是方法名（用空格替换下划线），该列的每行都以字符串形式展示出处。

你可以通过在该方法上（在 `polls/models.py` 中）使用 [`display()`](https://docs.djangoproject.com/zh-hans/4.2/ref/contrib/admin/#django.contrib.admin.display) 装饰器来改进，如下图所示：

`polls/models.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial07/#id8)

```python
from django.contrib import admin


class Question(models.Model):
    # ...
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
```

再次编辑文件 `polls/admin.py`，优化 `Question` 变更页：过滤器，使用 [`list_filter`](https://docs.djangoproject.com/zh-hans/4.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter)。将以下代码添加至 `QuestionAdmin`：

```
list_filter = ["pub_date"]
```

这样做添加了一个“过滤器”侧边栏，允许人们以 `pub_date` 字段来过滤列表

展示的过滤器类型取决你你要过滤的字段的类型。因为 `pub_date` 是类 [`DateTimeField`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#django.db.models.DateTimeField)，Django 知道要提供哪个过滤器：“任意时间”，“今天”，“过去7天”，“这个月”和“今年”。

这已经弄的很好了。让我们再扩充些功能:

```
search_fields = ["question_text"]
```

在列表的顶部增加一个搜索框。当输入待搜项时，Django 将搜索 `question_text` 字段。你可以使用任意多的字段——由于后台使用 `LIKE` 来查询数据，将待搜索的字段数限制为一个不会出问题大小，会便于数据库进行查询操作。

现在是给你的修改列表页增加分页功能的好时机。默认每页显示 100 项。[`变更页分页`](https://docs.djangoproject.com/zh-hans/4.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_per_page), [`搜索框`](https://docs.djangoproject.com/zh-hans/4.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields), [`过滤器`](https://docs.djangoproject.com/zh-hans/4.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter), [`日期层次结构`](https://docs.djangoproject.com/zh-hans/4.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.date_hierarchy), 和 [`列标题排序`](https://docs.djangoproject.com/zh-hans/4.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) 均以你期望的方式合作运行。

## 自定义后台界面和风格

在每个后台页顶部显示“Django 管理员”显得很滑稽。这只是一串占位文本。

不过，你可以通过 Django 的模板系统来修改。Django 的后台由自己驱动，且它的交互接口采用 Django 自己的模板系统。

### 自定义你的工程的模版

在你的工程目录（指包含 `manage.py` 的那个文件夹）内创建一个名为 `templates` 的目录。模板可放在你系统中任何 Django 能找到的位置。（谁启动了 Django，Django 就以他的用户身份运行。）不过，把你的模板放在工程内会带来很大便利，推荐你这样做。

打开你的设置文件（`mysite/settings.py`，牢记），在 [`TEMPLATES`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-TEMPLATES) 设置中添加 [`DIRS`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-TEMPLATES-DIRS) 选项：

`mysite/settings.py`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial07/#id9)

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

[`DIRS`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-TEMPLATES-DIRS) 是一个包含多个系统目录的文件列表，用于在载入 Django 模板时使用，是一个待搜索路径。

现在在 `templates`中创建一个`admin` 的目录，并将模板从 Django 本身源代码 （ django/contrib/admin/templates） 中默认的 Django 管理模板 `admin/base_site.html` 目录中复制到该目录中。

```shell
# Django 的源文件在哪里？
# 如果你不知道 Django 源码在你系统的哪个位置，运行以下命令：

$ python -c "import django; print(django.__path__)"
```

接着，用你网页站点的名字编辑替换文件内的 `{{ site_header|default:_('Django administration') }}` （包含大括号）。完成后，你应该看到如下代码：

```html
{% block branding %}
<h1 id="site-name"><a href="{% url 'admin:index' %}">Polls Administration</a></h1>
{% endblock %}
```

我们会用这个方法来教你复写模板。在一个实际工程中，你可能更期望使用 [`django.contrib.admin.AdminSite.site_header`](https://docs.djangoproject.com/zh-hans/4.2/ref/contrib/admin/#django.contrib.admin.AdminSite.site_header) 来进行简单的定制。

这个模板文件包含很多类似 `{% block branding %}` 和 `{{ title }}` 的文本。 `{%` 和 `{{` 标签是 Django 模板语言的一部分。当 Django 渲染 `admin/base_site.html` 时，这个模板语言会被求值，生成最终的网页，就像我们在 [教程第 3 部分](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial03/) 所学的一样。

注意，所有的 Django 默认后台模板均可被复写。若要复写模板，像你修改 `base_site.html` 一样修改其它文件——先将其从默认目录中拷贝到你的自定义目录，再做修改。

### 自定义你应用的模版

机智的同学可能会问： [`DIRS`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-TEMPLATES-DIRS) 默认是空的，Django 是怎么找到默认的后台模板的？因为 [`APP_DIRS`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-TEMPLATES-APP_DIRS) 被置为 `True`，Django 会自动在每个应用包内递归查找 `templates/` 子目录（不要忘了 `django.contrib.admin` 也是一个应用）。

我们的投票应用不是非常复杂，所以无需自定义后台模板。不过，如果它变的更加复杂，需要修改 Django 的标准后台模板功能时，修改 *应用* 的模板会比 *工程* 的更加明智。这样，在其它工程包含这个投票应用时，可以确保它总是能找到需要的自定义模板文件。

更多关于 Django 如何查找模板的文档，参见 [加载模板文档](https://docs.djangoproject.com/zh-hans/4.2/topics/templates/#template-loading)。

### 自定义后台主页

在类似的说明中，你可能想要自定义 Django 后台索引页的外观。

默认情况下，它展示了所有配置在 [`INSTALLED_APPS`](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#std-setting-INSTALLED_APPS) 中，已通过后台应用注册，按拼音排序的应用。你可能想对这个页面的布局做重大的修改。毕竟，索引页是后台的重要页面，它应该便于使用。

需要自定义的模板是 `admin/index.html`。（像上一节修改 `admin/base_site.html` 那样修改此文件——从默认目录中拷贝此文件至自定义模板目录）。打开此文件，你将看到它使用了一个叫做 `app_list` 的模板变量。这个变量包含了每个安装的 Django 应用。你可以用任何你期望的硬编码链接（链接至特定对象的管理页）替代使用这个变量。

# 8.工具栏及查看第三方包

## 安装Django调试工具栏

Django 调试工具栏是用于调试 Django Web 应用程序的有用工具。

工具栏可帮助您了解应用程序的功能并识别问题。它通过提供面板来提供有关当前请求和响应的调试信息来实现此目的。

```shell
$ python -m pip install django-debug-toolbar
```

与 Django 集成的第三方包需要一些安装后设置才能将它们与您的项目集成。通常，你需要将包的 Django 应用添加到你的 `INSTALLED_APPS` 设置中。有些软件包需要其他更改，例如对 URLconf （ `urls.py` ） 的添加



# 进阶指南：如何编写可重用的程序

## 可重用性

可重用性是 Python 的根本

```shell
一个 package 提供了一组关联的 Python 代码的简单复用方式。一个包（“模块”）包含了一个或多个 Python 代码文件。

一个包通过 import foo.bar 或 from foo import bar 的形式导入。一个目录（例如 polls）要成为一个包，它必须包含一个特定的文件 __init__.py，即便这个文件是空的。

Django 应用 仅仅是专用于 Django 项目的 Python 包。应用会按照 Django 规则，创建好 models, tests, urls, 以及 views 等子模块。

稍后，我们将解释术语 打包 ——为了方便其它人安装 Python 包的处理流程。我知道，这可能会使你感到一点点迷惑。
```

## 项目和可复用应用

前面教程中，我们的工程应是下面这样

```shell
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
    polls/
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
            0001_initial.py
        models.py
        static/
            polls/
                images/
                    background.gif
                style.css
        templates/
            polls/
                detail.html
                index.html
                results.html
        tests.py
        urls.py
        views.py
    templates/
        admin/
            base_site.html
```

为项目和应用程序设置单独的模板目录：所有属于 polls 应用程序的部分都在 `polls` 中。这使得应用程序自成一体，更容易放到一个新项目中。

目录 `polls` 现在可以被拷贝至一个新的 Django 工程，且立刻被复用。不过现在还不是发布它的时候。为了这样做，我们需要打包这个应用，便于其他人安装它。

## 安装必须环境

Python 打包的当前状态有点混乱，被各种工具弄得一团糟。在本教程中，我们将使用 setuptools 来构建我们的包。它是推荐的打包工具（与 `distribute` fork 合并）。我们还将使用 pip 来安装和卸载它。您应该立即安装这两个软件包。如果你需要帮助，可以参考如何使用 pip 安装 Django。您可以采用相同的方式进行安装 `setuptools` 。

## 打包你的应用

Python 的 *打包* 将以一种特殊的格式组织你的应用，意在方便安装和使用这个应用。Django 本身就被打包成类似的形式。对于一个小应用，例如 polls，这不会太难。

1. 首先，在你的Django项目目录外创建一个django-polls的文件夹，用于放polls
   ```shell
   为你的应用选择一个名字
   
   当为你的包选一个名字时，避免使用像 PyPI 这样已存在的包名，否则会导致冲突。当你创建你的发布包时，可以在模块名前增加 django- 前缀，这是一个很常用也很有用的避免包名冲突的方法。同时也有助于他人在寻找 Django 应用时确认你的 app 是 Django 独有的。
   
   应用标签（指用点分隔的包名的最后一部分）在 INSTALLED_APPS 中 必须 是独一无二的。避免使用任何与 Django contrib packages 文档中相同的标签名，比如 auth，admin，messages。
   ```

2. 将polls目录移入django-polls目录

3. 创建一个名为django-polls/README.rst的文件，包含以下内容：
   ```rst
   =====
   Polls
   =====
   
   Polls is a Django app to conduct web-based polls. For each question,
   visitors can choose between a fixed number of answers.
   
   Detailed documentation is in the "docs" directory.
   
   Quick start
   -----------
   
   1. Add "polls" to your INSTALLED_APPS setting like this::
   
       INSTALLED_APPS = [
           ...,
           "polls",
       ]
   
   2. Include the polls URLconf in your project urls.py like this::
   
       path("polls/", include("polls.urls")),
   
   3. Run ``python manage.py migrate`` to create the polls models.
   
   4. Start the development server and visit http://127.0.0.1:8000/admin/
      to create a poll (you'll need the Admin app enabled).
   
   5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.
   ```

4. 创建一个django-polls/LICENSE文件，选择一个非本教程使用的授权协议，但是要足以说明发布代码没有授权证书是不可能的，Django和很多兼容Django的应用是以BSD授权协议发布的，不过，你可以自己选择一个授权协议。只要确定你选择的协议能够限制未来会使用你的代码的人

5. 接下来我们将创建 `pyproject.toml`、`setup.cfg` 和 `setup.py` 文件，详细说明如何构建和安装该应用程序。对这些文件的全面解释超出了本教程的范围，但 [setuptools 文档](https://setuptools.pypa.io/en/latest/) 有很好的解释。创建 `django-polls/pyproject.toml`、`django-polls/setup.cfg` 和 `django-polls/setup.py` 文件，内容如下：

   `django-polls/pyproject.toml`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/reusable-apps/#id2)

   ```toml
   [build-system]
   requires = ['setuptools>=40.8.0']
   build-backend = 'setuptools.build_meta'
   ```

6. 默认情况下，包中仅包含 Python 模块和包。若要包含其他文件，我们需要创建一个 `MANIFEST.in` 文件。上一步中引用的 `setuptools` 文档更详细地讨论了此文件。要包含模板、和 `README.rst` 我们的 `LICENSE` 文件，请创建一个包含以下内容的文件 `django-polls/MANIFEST.in` ：`django-polls/MANIFEST.in`[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/reusable-apps/#id5)
   ```in
   include LICENSE
   include README.rst
   recursive-include polls/static *
   recursive-include polls/templates *
   ```

   

7. 在应用中包含详细文档是可选的，但我们推荐你这样做。创建一个空目录 `django-polls/docs` 用于未来编写文档。额外添加一行至 `django-polls/MANIFEST.in`：

   ```
   recursive-include docs *
   ```

   注意，现在 `docs` 目录不会被加入你的应用包，除非你往这个目录加几个文件。许多 Django 应用也提供他们的在线文档通过类似 [readthedocs.org](https://readthedocs.org/) 这样的网站。

8. 试着用 `python setup.py sdist` 构建你的应用包（在 `django-polls` 目录运行）。这将创建一个名为 `dist` 的目录，并构建你的新应用包，`django-polls-0.1.tar.gz`

更多关于打包的信息，见 Python 的 [关于打包和发布项目的教程](https://packaging.python.org/tutorials/packaging-projects/)。

## 使用你自己的包名

由于我们把 `polls` 目录移出了项目，所以它无法工作了。我们现在要通过安装我们的新 `django-polls` 应用来修复这个问题。

```shell
作为用户库安装

以下步骤将 django-polls 以用户库的形式安装。与安装整个系统的软件包相比，用户安装具有许多优点，例如可在没有管理员访问权的系统上使用，以及防止应用包影响系统服务和其他用户。

请注意，按用户安装仍然会影响以该用户身份运行的系统工具的行为，因此使用虚拟环境是更可靠的解决方案（请参见下文）。
```

1. 安装这个包，使用pip
   ```shell
   python -m pip install --user django-polls/dist/django-polls-0.1.tar.gz
   ```

2. 幸运的话，你的 Django 项目应该再一次正确运行。启动服务器确认这一点。

3. 卸载包
   ```shell
   python -m pip uninstall django-polls
   ```

## 发布你的应用

## 发布你的应用[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/reusable-apps/#publishing-your-app)

现在，你已经对 `django-polls` 完成了打包和测试，准备好向世界分享它！如果这不是一个例子应用，你现在就可以这样做。

- 通过邮件将你的包发送给朋友。
- 将这个包上传至你的网站。
- 将你的包发布至公共仓库，比如 [the Python Package Index (PyPI)](https://pypi.python.org/pypi)。 [packaging.python.org](https://packaging.python.org/) 有一个不错的 [教程](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives) 说明如何发布至公共仓库。

## 通过虚拟环境安装 Python 包[¶](https://docs.djangoproject.com/zh-hans/4.2/intro/reusable-apps/#installing-python-packages-with-a-virtual-environment)

早些时候，我们以用户库的形式安装了投票应用。这样做有一些缺点。

- 修改用户库会影响你系统上的其他 Python 软件。
- 你将不能运行此包的多个版本（或者其它用有相同包名的包）。

通常，只有在维护多个 Django 项目时才会出现这些情况。当这样做时，最好的解决方法是使用 [venv](https://docs.python.org/3/tutorial/venv.html)。使用此工具，你可以维护多个隔离的 Python 环境，每个环境都有其自己的库和包命名空间的副本。































