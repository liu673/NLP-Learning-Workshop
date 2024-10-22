



# HTTPS网站

普通 HTTP 站点的协议与数据以明文方式在网络上传输，而 HTTPS（Hyper Text Transfer Protocol over Secure Socket Layer）是以安全为目标的 HTTP 通道，即在 HTTP 下加入 SSL 层，通过 SSL 达到数据加密及身份认证的功能。

目前大多数网站通过 OpenSSL 工具包搭建 HTTPS 站点，其步骤如下：

- 在服务器中安装 OpenSSL 工具包。
- 生成 SSL 密钥和证书。
-  将证书配置到 Web 服务器。
-  在客户端安装 CA 证书。

# Django

## 综述

Django 的 Model 层自带数据库 ORM 组件，使开发者无须学习其他数据库访问技术（DBI、SQLAlchemy 等）。

### 组成结构

Django 是遵循 MVC 架构的 Web 开发框架，其主要由以下几部分组成。

- **管理工具（Management）**：一套内置的创建站点、迁移数据、维护静态文件的命令工具。
- **模型**：提供数据访问接口和模块，包括数据字段、元数据、数据关系等的定义及操作。
- **视图**：Django 的视图层封装了 HTTP Request 和 Response 的一系列操作和数据流，其主要功能包括 URL 映射机制、绑定模板等。
- **模板（Template）**：是一套 Django 自己的页面渲染模板语言，用若干内置的 tags 和 filters定义页面的生成方式。
-  **表单（Form）**：通过内置的数据类型和控件生成 HTML 表单。
-  **管理站（Admin）**：通过声明需要管理的 Model，快速生成后台数据管理网站。

## 实战

### 建立项目

```shell
# 在某个目录下建立开发项目，以下是建立一个叫做djangosite的项目
django-admin startproject djangosite
```

该命令在当前目录中建立了一个子目录 djangosite，并在其中生成了 Django 开发的默认文件，djangosite 的目录内容如下：

```
djangosite/ 
	manage.py    是 Django 用于管理本项目的命令行工具，之后进行				 站点运行、数据库自动生成、静态文件收集等都要通过				  该文件完成。
	djangosite/ 
		__init__.py 	告诉 Python 该目录是一个 Python 						包，其中暂无内容。
		
		settings.py 	Django 的项目配置文件。默认时，在其中						  定义了本项目引用的Django 组件、							Django 项目名等。在之后的开发中，还需						  在其中配置数据库参数、导入的其他 								Python 包等信息。
		
		urls.py 		维护项目的URL路由映射，即定义客户端访						问的URL由哪一个Python模块解释并提供反						   馈。在默认情况下，其中只定义								了“/admin”即管理员站点的解释器。
		
        wsgi.py 		定义 WSGI 的接口信息，用于与其他 Web 						服务器集成，一般本文件在生成后无须改动
```

### 建立应用

manage.py 是建立项目时在项目目录中产生的命令行工具，startapp 是命令的关键字，

```shell
cd djangosite 
python manage.py startapp app
```

命令完成后会在项目目录中建立如下目录及文件结构：

```
app/ 
	__init__.py 	其中暂无内容，该文件的存在使得 app 成为一个 					 Python 包。
	admin.py 		管理站点模型的声明文件，默认为空。
	
	apps.py 		应用信息定义文件。在其中生成了类 							AppConfig，该类用于定义应用名等 Meta数据

    models.py 		添加模型层数据类的文件。
    tests.py 		测试代码文件。
    views.py		定义 URL 响应函数。
    migrations/ 	用于在之后定义引用迁移功能。
    	__init__.py 
```

### 基本视图

- 首先在 djangosite/app/views.py 中建立一个路由响应函数：
  ```python
  from django.http import HttpResponse 
  def welcome(request): 
      return HttpResponse("<h1>Welcome to my tiny twitter!</h1>")
  # 该代码定义了一个函数 welcome()，简单地返回一条被 HttpResponse()函数封装的 Welcome信息。
  ```

- 要通过 URL 映射将用户的 HTTP 访问与该函数绑定起来。 

  djangosite/app/目录中新建一个 urls.py 文件，管理应用 app 中的所有 URL 映射

  ```python
  from django.urls import path, re_path as url
  from .views import welcome
  
  urlpatterns = [
      url(r'', welcome, name="first-url"),
  ]
  ```

- 在项目 URL 文件 djangosite/urls.py 的 urlpatterns 中增加一项，声明对应用 app 中 urls.py文件的引用，
  ```python
  from django.contrib import admin
  from django.urls import path, include, re_path as url
  
  urlpatterns = [
      url(r'^app/', include('app.urls')),
      path("admin/", admin.site.urls),
  ]
  # 首先通过 import 语句引入 django.conf.urls.include()函数，之后在 urlpatterns 列表中增加一个路径 app/，将其转接到 app.urls 包，即 djangosite/app/urls.py 文件。这样，通过 include()函数就将两个 urlpatterns 连接了起来。
  ```

### Web服务器

```shell
cd djangosite 
python manage.py runserver
```

### 模型类

Model 层的处理，即设计和开发信息发布的数据访问层

#### 1.配置项目INSTALLED_APPS

要在 djangosite 项目的 settings.py 中告诉 Django 需要安装应用 app 中的模型，则方法是打开 djangosite/settings.py 文件，找到其中的 INSTALLED_APPS 数组，在其中添加应用 app 的Config 类，代码如下：
```django
INSTALLED_APPS = [ 
    'app.apps.AppConfig', # 此行新增
    'django.contrib.admin', 
    'django.contrib.auth', 
    'django.contrib.contenttypes', 
    'django.contrib.sessions', 
    'django.contrib.messages', 
    'django.contrib.staticfiles', 
]
# 上述代码中的app.apps.AppConfig声明的是djangosite/app/apps.py中自动生成的AppConfig 类。
```

#### 2.模型定义

打开 djangosite/app/models.py，在其中新建一个模型类 Moment 用来定义信息发布表，

```python
from django.db import models 
class Moment(models.Model): 
    content = models.CharField(max_length=200) 
    user_name = models.CharField(max_length = 20) 
    kind = models.CharField(max_length = 20)

# 在第 1 行中引入了 django.db.models 类，所有 Django 模型类必须继承自它。之后定义了该类的子类 Moment，在其中定义了 3 个字符串类型的字段：content 保存消息的内容、user_name保存发布人的名字、kind 保存消息的类型。
```

#### 3.生成数据移植文件

Django 的术语“生成数据移植文件”（makemigrations）是指将 models.py 中定义的数据表转换成数据库生成脚本的过程。该过程通过命令行工具 manage.py 完成，具体的命令及输出如下：

```shell
cd djangosite 
python manage.py makemigrations app
```

> 通过输出可以看到完成了模型 Moment 的建立。输出中的 0001_initial.py 是数据库生成的中间文件，通过它也可以知道当前的数据库版本；该文件及以后的所有 migration 文件都存在于目录 djangosite/app/migrations/中。

在 makemigrations 的过程中，Django 会对比 models.py 中的模型与已有数据库之间的差异，如果没有差异则不会做任何工作，比如再次执行 makemigrations 操作时将产生如下输出：
```shell
# python manage.py makemigrations app 
No changes detected in app 'app'
```

如果对 models.py 做任何修改，则在下一次 makemigrations 的时候会将修改的内容同步到数据库中。比如，将 Moment 类的 content 字段长度从 200 修改为 300 后，再次执行 makemigrations的结果如下
```shell
# python manage.py makemigrations app 
Migrations for 'app': 
 app/migrations/0002_auto_20180726_0411.py 
 - Alter field content on moment

# 在其过程中产生了新的中间文件 0002_auto_20180726_0411.py
```

#### 4.移植到数据库

在模型的修改过程中可以随时调用 makemigrations 生成中间移植文件。而当需要使移植文件生效、修改真实的数据库 schema 时，则需要通过 manage.py 的 migrate 命令使修改同步到数据库中。

```shell
# cd djangosite 
# python manage.py migrate
```

### 表单视图

是设计和开发信息录入页面。该页面的基本功能为：提供输入界面，让用户输入名字、文本消息内容、选择消息类型，用户提交后网页自动设置该信息的时间并保存到数据库中。

#### 1.定义表单类

建立表单类文件 djangosite/app/forms.py，在其中定义表单类 MomentForm。

```python
from django.forms import ModelForm 
from app.models import Moment 
class MomentForm(ModelForm): 
    class Meta: 
    model = Moment 
    fields = '__all__' # 引入所有字段
   
# 引入 django.forms.ModelForm 类，该类是所用 Django 表单类的基类。
# 引入在本应用 models.py 中定义的 Moment 类，以便在后面的表单类中关联 Moment 类。
# 定义表单类 MomentForm，在其中定义子类 Meta。在 Meta 中声明与本表单关联的模型类及其字段。
# Fields 字段可以设为__all__，也可以用列表形式声明所要导入的属性，比如：fields=('content', 'user_name', 'kind')。
```

#### 2.修改模型类

如果要使用户能够以单选的方式设置消息类型，则需要在 models.py 文件中定义单选枚举值，并与模型类 Moment 相关联。把 djangosite/app/models.py 修改为如下：

```python
from __future__ import unicode_literals 
from django.db import models 
# 新增元组用于设置消息类型枚举项
KIND_CHOICES = ( 
    ('Python 技术', 'Python 技术'), 
    ('数据库技术', '数据库技术'), 
    ('经济学', '经济学'), 
    ('文体资讯', '文体资讯'), 
    ('个人心情', '个人心情'), 
    ('其他', '其他'), 
) 
class Moment(models.Model): 
    content = models.CharField(max_length=300) 
    user_name = models.CharField(max_length = 20, default = '匿名') 
    # 修改 kind 定义，加入 choices 参数
    kind = models.CharField(max_length = 20, choices = KIND_CHOICES, default = KIND_CHOICES[0])
    
# 主要修改内容是：
# 为 kind 字段增加了消息类型枚举项；
# 为 user_name 和 kind 字段用 default 属性配置了默认值。
```

> 注意：因为本次编辑导致模型层发生变化，所以需要用 manage.py 命令行工具运行makemigrations 和 migrate 命令来更新数据库的定义。
> ```python
> python manage.py makemigrations app
> python manage.py migrate
> ```

#### 3.开发模版文件

模板是 Python Web 框架中用于产生 HTML、XML 等文本格式文档的术语。模板文件本身也是一种文本文件，开发者需要手工对其编辑和开发。建立目录 djangosite/app/templates，在其中新建模板文件 moments_input.html，文件的内容如下：

```htm
<!DOCTYPE html> 
<html> 
    <head> 
    	<title>消息录入页面</title> 
    </head> 
    <body> 
    	<form action="?" method="post"> 
            <fieldset>
                <legend>请输入并提交</legend> 
                    {{ form.as_p }} 
                    <input type="submit" value="submit" /> 
            </fieldset> 
		</form> 
	</body> 
</html>
```

模板文件以 HTML 格式为基本结构，其中的模板内容用大括号标识。本例用{{ form.as_p }}定义表单类 MomentForm 的输入字段。

#### 4.开发视图

开发视图函数使得表单类和页面模板衔接起来。打开 djangosite/app/views.py 文件，在其中加入如下函数：

```python
import os 
from app.forms import MomentForm 
from django.http import HttpResponseRedirect 
from django.urls import reverse 
from django.shortcuts import render 

def moments_input(request): 
    if request.method == 'POST': 
        form = MomentForm(request.POST) 
        if form.is_valid(): 
            moment = form.save() 
            moment.save() 
            return HttpResponseRedirect(reverse('first-url')) 
    else: 
        form = MomentForm() 
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    return render(request, os.path.join(PROJECT_ROOT, 'app/templates', 'moments_input.html'), {'form': form})

# 在代码中新增了视图函数 moments_input()，该函数定义了两种访问方式的不同处理方法。
# 如果是用户的 Post 表单提交，则保存 moment 对象，并重定向到欢迎页面。其中 reverse()函数根据映射名称找到正确的 URL 地址，本例中使用的是在 djangosite/app/urls.py 中配置过的名称'first-url'。
# 如果是普通的访问，则返回 moments_input.html 模板的渲染结果作为 HTTP Response。注意，render()的第 3 个参数将 form 作为参数传给了模板，这样在模板文件中才能访问该 MomentForm 的实例。
```

djangosite/app/urls.py 文件中增加该视图函数的路由映射，内容如下：

```python
urlpatterns = [ 
    url(r'moments_input', views.moments_input), # 本行新增
    url(r'', views.welcome, name=’first-url’), 
]
```



### 使用管理界面

Django 管理界面是一个通过简单的配置就可以实现的数据模型后台的 Web 控制台。管理界面通常是给系统管理员使用的，以完成元数据的输入、删除、查询等工作。

- 首先将管理界面需要管理的模型类添加到 djangosite/app/admin.py 文件中，具体如下：
  ```python 
  from django.contrib import admin 
  from .models import Moment 
  
  admin.site.register(Moment)
  # 本文件中只要通过 admin.site.register()函数逐个声明要管理的模型类即可。
  ```

- 在第 1 次访问管理界面之前，需要通过 manage.py 工具的 createsuperuser 命令建立管理员用户。在命令运行的过程中按照提示输入管理员的用户名、邮箱地址、密码：
  ```shell
  # cd djangosite 
  # python manage.py createsuperuser
  ```

  

## Django模型层

Django 模型层是 Django 框架自定义的一套独特的 ORM 技术。

### 基本操作

使用 Django 模型开发的首要任务就是定义模型类及其属性。每个模型类都可以被映射为数据库中的一个数据表，而类属性被映射为数据字段，除此之外，数据库表的主键、外键、约束等也通过类属性完成定义

#### 1.模型类定义

```python
from django.db import models 

class ModelName(models.Model): 
     field1 = models.XXField(…) 
     field2 = models.XXField(…) 
     … 
     class Meta: 
         db_table = … 
         other_metas = …
```

- 所有 Django 模型继承自 django.db.models.Model 类。

- 通过其中的类属性定义模型字段，模型字段必须是某种 models.XXField 类型。

- 通过模型类中的 Meta 子类定义模型元数据，比如数据库表名、数据默认排序方式等。

Meta 类的属性名由 Django 预定义，常用的 Meta 类属性汇总如下

- **abstract**：True or False，标识本类是否为抽象基类。

- **app_label**：定义本类所属的应用，比如 app_label = 'myapp'。

- **db_table**：映射的数据表名，比如 db_table = 'moments'。

  > 如果 Meta 中不提供 db_table 字段，则 Django 会为模型自动生成数据表名，生成的格式为“应用名_模型名”，比如应用 app 的模型 Comment 的默认数据表名为 app_comment。

- **db_tablespace**：映射的表空间名称。表空间的概念只在某些数据库如 Oracle 中存在，不存在表空间概念的数据库将忽略本字段。

- **default_related_name**：定义本模型的反向关系引用名称，默认与模型名一致。

- **get_latest_by**：定义按哪个字段值排列以获得模型的开始或结束记录，本属性值通常指向一个日期或整型的模型字段。

- **managed**：True 或 False，定义 Django 的 manage.py 命令行工具是否管理本模型。本属性默认为 True，如果将其设为 False，则运行 python manage.py migrate 时将不会在数据库中生成本模型的数据表，所以需要手工维护数据库的定义。

- **order_with_respect_to**：定义本模型可以按照某外键引用的关系排序。

- **ordering**：本模型记录的默认排序字段，可以设置多个字段，默认以升序排列，如果以降序排列则需要在字段名前加“负号”。比如，如下定义按 user_name 升序和 pub_date降序排列

  ```python
  class Meta:
      ordering = ["user_name", "-pub_date"]
  ```

- **default_permissions**：模型操作权限，默认为default_permisstions= ('add', 'change', 'delete')。

- **proxy**：True 或 False，本模型及所有继承自本模型的子模型是否为代理模型。

- **required_db_features**：定义底层数据库所必需具备的特性。比如 required_db_features= ['gis_enabled']只将本数据模型生成在满足 gis_enabled 特性的数据库中。

- **required_db_vendor**：定义底层数据库的类型，比如 SQLite、PostgreSQL、MySQL、Oracle。如果定义了本属性，则模型只能在其声明的数据库中被维护。

- **unique_together**：用来设置的不重复的字段组合，必须唯一（可以将多个字段做联合唯一）。

  ```python
  class Meta:
      unique_together = (("user_name", "pub_date"))
  
  # 上述代码定义每个 user_name 在同一个 pub_date 中只能有一条数据表记录。因为unique_together 本身是一个元组，所以可以设置多个这样的唯一约束。
  ```

- **index_together**：定义联合索引的字段，可以设置多个。

  ```python
  class Meta:
      index_together = [["pub_date", "deadline"]]
  ```

- **verbose_name**：指明一个易于理解和表述的单数形式的对象名称。如果这个值没有被设置，则 Django 将会使用该 model 类名的分词形式作为它的对象表述名，即 CamelCase将会被转换为 camel case。

-  **verbose_name_plural**：指明一个易于理解和表述的复数形式的对象名称。

#### 2.普通字段类型

普通字段是指模型类中除外键关系外的数据字段属性。数据字段为 Django 使用模型时提供如下信息。

- 在数据库中用什么类型定义模型字段，比如 INTEGER、VARCHAR 等。
- 用什么样的 HTML 标签显示模型字段，比如<input type="radio">等。
- 需要什么样的 HTML 表单数据验证。

所有数据字段的属性必须继承自抽象类 django.db.models.Field，开发者可以定义自己继承自该类的字段类型，也可以使用 Django 预定义的一系列 Field 子类。常用的 Django 预定义字段类型描述如下。

- **AutoField**：一个自动递增的整型字段，添加记录时它会自动增长。AutoField 字段通常只用于充当数据表的主键；如果在模型中没有指定主键字段，则 Django 会自动添加一个 AutoField 字段。
- **BigIntegerField**：64 位整型字段。
- **BinaryField**：二进制数据字段，只能通过 bytes 对其进行赋值。
- **BooleanField**：布尔字段，相对应的 HTML 标签是<input type="checkbox">。
- **CharField**：字符串字段，用于较短的字符串，相对应的 HTML 标签是单行输入框<input type="text">。
- **TextField**：大容量文本字段，相对应的 HTML 标签是多行编辑框<textarea>。
- **CommaSeparatedIntegerField**：用于存放逗号分隔的整数值，相对于普通的 CharField，它有特殊的表单数据验证要求。
- **DateField**：日期字段，相对应的 HTML 标签是<input type="text">、一个 JavaScript 日历和一个“Today”快捷按键。有下列额外的可选参数：auto_now，当对象被保存时，将该字段的值设置为当前时间；auto_now_add，当对象首次被创建时，将该字段的值设置为当前时间。
- **DateTimeField**：类似于 DateField，但同时支持时间输入。
- **DurationField**：存储时间周期，用 Python 的 timedelta 类型构建。
- **EmailField**：一个带有检查 Email 合法性的 CharField。
- **FileField**：一个文件上传字段。在定义本字段时必须传入参数 upload_to，用于保存上载文件的服务器文件系统的路径。这个路径必须包含 strftime formatting，该格式将被上载文件的 date/time 替换。
- **FilePathField**：按目录限制规则选择文件，定义本字段时必须传入参数 path，用以限定目录。
- **FloatField**：浮点型字段。定义本字段时必须传入参数 max_digits 和 decimal_places，用于定义总位数（不包括小数点和符号）和小数位数。
- **ImageField**：类似于 FileField，同时验证上传对象是否是一个合法图片。它有两个可选参数，即 height_field 和 width_field。如果提供这两个参数，则图片将按提供的高度和宽度规格保存。该字段要求安装 Python Imaging 库。
- **IntegerField**：用于保存一个整数。
- **IPAddressField**：一个字符串形式的 IP 地址，比如“129.23.250.2”。
- **NullBooleanField**：类似于 BooleanField，但比其多一个 None 选项。
- **PhoneNumberField**：带有美国风格的电话号码校验的 CharField（格式为×××-×××-××××）。
- **PositiveIntegerField**：只能输入非负数的 IntegerField。
- **SlugField**：只包含字母、数字、下画线和连字符的输入字段，它通常用于 URL。
- **SmallIntegerField**：类似于 IntegerField，但只具有较小的输入范围，具体范围依赖于所使用的数据库。
- **TimeField**：时间字段，类似于 DateTimeField，但只能表达和输入时间。
- **URLField**：用于保存 URL。
- **USStateField**：美国州名的缩写字段，由两个字母组成。
- **XMLField**：XML 字符字段，是具有 XML 合法性验证的 TextField。

#### 3.常用字段参数

每个字段类型都有一些特定的 HTML 标签和表单验证参数，比如 height_field、path 等。但同时有一些每个字段都可以设置的公共参数，比如通过 **primary_key 参数**可以设置一个模型的主键字段：
```python
from django.db import models

class Comment(models.Model): 
	id = models.AutoField(primary_key=True)
```

其他这样的参数如下：

- **null**：定义是否允许相对应的数据库字段为 Null，默认设置为 False。

- **blank**：定义字段是否可以为空。读者需要区分 blank 与 null 的区别。null 是一个数据库中的非空约束；而 blank 用于字段的 HTML 表单验证，即判断用户是否可以不输入数据。

- **choices**：定义字段的可选值。本字段的值应该是一个包含二维元素的元组。元组的每个元素中的第 1 个值是实际存储的值，第 2 个值是 HTML 页面中进行选择时显示的值。

  ```python
  from django.db import models 
  LEVELS = ( 
      ('1', 'Very good'), 
      ('2', 'Good'), 
      ('3', 'Normal'), 
      ('4', 'Bad'), 
  ) 
  class Comment(models.Model): 
      id = models.AutoField(primary_key=True) 
      level = models.CharField(max_length=1, choices=LEVELS)
  
  # 上述代码中定义了level字段用于让用户选择满意度，其中1、2、3、4 是在数据库中实际存储的数据，而 Very good、Good、Normal、Bad 等是在 HTML 的列表控件中提供给用户的选项。
  ```

- **default**：设定默认值，例如 default="please input here"。

- **help_text**：HTML 页面中输入控件的帮助字符串。

- **primary_key**：定义字段是否为主键，为 True 或 False。

- **unique**：是否为字段定义数据库的唯一约束

- 除了这些有名称的字段参数，Django 中的所有 Field 数据类型还有一个无名参数，可以设置该字段在 HTML 页面中的人性化名称，比如：
  ```python 
  class Comment(models.Model): 
      id = models.AutoField(primary_key=True) 
      level = models.CharField("请为本条信息评级", max_length=1, choices=LEVELS)
  
  # 本例中开发者为 level 字段定义了人性化名称“请为本条信息评级”，如果不设置本参数，则字段的名称本身将被显示在 HTML 页面中作为输入提示。
  ```

#### 4.基本查询

```shell
python manage.py shell

# 查询models里面的Comment
from app.models import Comment

Comment.objects.all()
```

Django 有两种过滤器用于筛选记录。

- filter(**kwargs)：返回符合筛选条件的数据集。
- exclude(**kwargs)：返回不符合筛选条件的数据集。

> 多个 filter 和 exclude 可以连接在一起查询，比如 Comment.objects.filter(pub_ date_year ==2018).exclude(pub_date_month=1).exclude(n_visits_exact=0)查询所有 2018 年非 1 月的 n_visits 不为 0 的记录。

意代码中的 pub_date__year，它不是模型中定义的一个字段，而是 Django 定义的一种独特的**字段查询（field lookup）**表达方式，本例中该查询的含义是“pub_date 字段的 year属性为 2018”。field lookup 的基本表现形式是：

```shell
字段名称_谓词
# 即由“字段名称__谓词”来表达查询条件。
```

**谓词表**

| 谓词       | 含义               | 示例                                                         | 等价SQL语句                                                  |
| ---------- | ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| exact      | 精确等于           | Comment.objects.filter(id__exact=14)                         | select * from Comment where id=14                            |
| iexact     | 大小写不敏感的等于 | Comment.objects.filter(headline__iexact=’I like this’)       | select * from Comment where upper(headline)=’I LIKE THIS’    |
| contains   | 模糊匹配           | Comment.objects.filter(headline__contains=’good’)            | select * from Comment where headline like “%good%”           |
| in         | 包含               | Comment.objects.filter(id__in=[1,5,9])                       | select * from Comment where id in (1,5,9)                    |
| gt         | 大于               | Comment.objects.filter(n_visits__gt=30)                      | select * from Comment where n_visits>30                      |
| gte        | 大于等于           | Comment.objects.filter(n_visits__gte=30)                     | select * from COmment where n_visits>=30                     |
| lt         | 小于               |                                                              |                                                              |
| lte        | 小于等于           |                                                              |                                                              |
| startswith | 以…开头            | Comment.objects.filter(body_text__startswith=”Hello”)        | select * from Comment where body_text like ‘Hello%’          |
| endswith   | 以…结尾            |                                                              |                                                              |
| range      | 在…范围内          | start_date=datetime.date(2015,1,1) end_date=datetime.date(2015.2.1) Comment.objects.filter(   pub_date__range=(start_date,end_date) ) | select * from Comment where pub_date between ‘2015-1-1’ and ‘2015-2-1’ |
| year       | 年                 | Comment.objects.filter(   pub_date__year=2015 )              | select * from Comment where pub_date between ‘2015-1-1 0:0:0’ and ‘2015-12-31 23:59:59’ |
| month      | 月                 |                                                              |                                                              |
| day        | 日                 |                                                              |                                                              |
| week_day   | 星期几             |                                                              |                                                              |
| isnull     | 是否为空           | Comment.objects.filter(   pub_date__isnull=True )            | select * from Comment where pub_date is NULL                 |

 除了 all()、filter()、exclude()等返回数据集的函数，Django 还提供了 get()用于查询单条记录，

```shell
Comment.objects.get(id_exact = 1)
```

Django 还提供了用于查询指定条数的数据集的下标操作，该特性使得 Django 模型能够支持标准 SQL 中的 LIMIT 和 OFFSET 谓词。比如：

```shell
>>> Comment.objects.all()[:10] # 返回数据集，查询前 10 条记录
>>> Comment.objects.all()[10: 20] # 返回数据集，查询从第 11～20 条记录
>>> Comment.objects.all()[1] # 返回单条记录，查询第 2 条记录（index 从 0 开始）
```

Django 还提供了 order_by 操作，比如：

```shell
>>>Comment.objects.order_by('headline') #返回数据集，并按照 headline 字段排序
```

#### 5.数据保存与删除

Django 的一个较大优势是定义了一个统一的方法 save()，用于完成模型的 Insert 和 Update 操作。

```python
# 新增记录
>>> newObj = Comment(headline = "I like this", body_text = "..", 
 pub_date = datetime.datetime.now(), n_visits = 0) 
>>> newObj.save() 
# 打印新增对象的主键
>>> print(newObject.id) 
13 
# 修改记录数据
>>> newObj.body_text = "This comment is just what I want" 
>>> newObj.save() 
# 打印主键，与新增后的 id 相同
>>> print(newObj.id) 
13
```

```python
# 删除所有 2017 年的记录
>>>Comment.objects.filter(pub_date__year=2017).delete()

# 删除 id=3 的单条记录
>>> Comment.objects.get(id=3).delete()
```

### 关系操作

利用数据表之间的关系进行数据建模和业务开发是关系数据库最主要的功能。Django 模型层对 3 种关系模型（1∶1、1∶*N*、*M*∶*N*）都有强大的支持。

#### 1.一对一关系

在 SQL 语言中，一对一关系通过在两个表之间定义相同的主键来完成。在 Django 模型层，可以在任意一个模型中定义 **OneToOneField** 字段，并定义相互之间的一对一关系。如下代码在模型 Account 和 Contact 之间定义了一对一关系：

```python
from django.db import models 
class Account(models.Model): 
    user_name = models.CharField(max_length = 80) 
    password = models.CharField(max_length = 255) 
    reg_date = models.DateField() 
    def __unicode__(self): 
    	return "Account: %s" % self.user_name 

class Contact(models.Model): 
    account = models.OneToOneField( 
        Account, 
        on_delete=models.CASCADE, 
        primary_key=True, 
    ) 
    zip_code = models.CharField(max_length=10) 
    address = models.CharField(max_length=80) 
    mobile = models.CharField(max_length=20) 
    def __unicode__(self): 
    	return "%s, %s" % (self.accout.user_name, mobile)
    
# 两个模型的关系通过 Contact 模型中的 account 字段进行定义。
# OneToOneField()的第 1 个参数定义被关联的模型名。
# on_delete 参数定义当被关联模型（Account）的记录被删除时本模型的记录如何处理，models.CASCADE 用于定义此时本记录（Contact）也被删除。
# 每个模型的__unicode__()函数用于定义模型的显示字符串。
```

```python
>>> a1 = Account(user_name = "david") 
>>> a1.save() # 保存一个 Account 记录
>>> a2 =Account(user_name = "Rose") 
>>> a2.save() 
 #用 a1 初始化 Contact 的 account 字段，并保存
>>> c1 = Contact(account = a1, mobile = "13912345000") 
>>> c1.save() # 保存 Contact 记录

>>> print(a1) # 打印 a1 
<Account: david> 
>>> print(c1) # 打印 c1 
<Contact: david, 13912345000> 
>>> print(a1.contact) # 通过关系打印，与打印 c1 的结果相同
<Contact: david, 13912345000> 
>>> print(c1.account) # 通过关系打印，与打印 a1 的结果相同
<Account: david> 
# 因为 a2 没有与任何 Contact 建立过关系，所以它没有 contact 属性/字段
>>> print(hasattr(a2, 'contact')) 
False 
# 由于定义了 on_delete=models.CASCADE，因此如下语句在从数据库中删除 a1 对象的同时，也将 c1 对象从数据库中删除
>>> a1.delete()
```

#### 2.一对多关系

SQL 语言中，1∶*N* 关系通过在“附表”中设置到“主表”的外键引用来完成。在 Django模型层，可以用 **models.ForeignKey** 类型的字段定义外键。如下代码在模型 Account 和 Contact之间定义了一对多关系：

```python
from django.db import models 
class Account(models.Model): 
    user_name = models.CharField(max_length = 80) 
    password = models.CharField(max_length = 255) 
    reg_date = models.DateField() 
    def __unicode__(self): 
    	return "Account: %s" % self.user_name
    
class Contact(models.Model): 
    account = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE
    ) 
    zip_code = models.CharField(max_length=10) 
    address = models.CharField(max_length=80) 
    mobile = models.CharField(max_length=20) 
    def __unicode__(self): 
   		return "%s, %s" % (self.accout.user_name, mobile)
```

上述代码与一对一关系的唯一不同是用 models.ForeignKey 定义了 Contact 模型中的 account 字段。这样，每个 Account 对象就可以与多个 Contact 对象相关联了。对模型应用代码的演示如下：

```python
>>> a1 = Account(user_name = "Rose") 
>>> a1.save() # 保存一个 Account 记录

# 为 a1 建立两个 Contact 关联对象
>>> c1 = Contact(account = a1, mobile = "13912345001") 
>>> c1.save() # 保存 Contact 记录
>>> c2 = Contact(account = a1, mobile = "13912345002") 
>>> c2.save() # 保存 Contact 记录

>>> print(c1.account) # 从附模型对象中找到主模型对象
<Account: Rose> 
>>> print(c2.account) # 从附模型对象中找到主模型对象
<Account: Rose> 

>>> print(a1.contact_set) # 从主模型对象中找到附模型对象
[<Contact: Rose, 13912345001>, <Contact: Rose, 13912345002>] 
>>> print(a1.contact_set.count()) # 从主模型对象中找到所关联附模型对象的数量
2 

# 由于定义了 on_delete=models.CASCADE，因此如下语句在从数据库中删除 a1 对象的同时，也将 c1 和 c2 对象从数据库中删除
>>> a1.delete()
```

在一对多关系中，每个主模型对象可以关联多个子对象，所以本例中从主模型 Account 对象中寻找附模型 Contact 的属性是 contact_set，即通过一个**集合返回关联结果**。

> 技巧：xxxx_set 是 Django 设定的通过主模型对象访问附模型对象集合的属性名。

#### 3.多对多关系

-  SQL 语言中，*M*∶*N* 关系通过建立一个中间关系表来完成，该中间表中定义了到两个主表的外键。所以在 Django 模型层中，开发者也可以选择用两个 1∶*N* 关系来定义 *M*∶*N* 关系。这种方式同样可以通过 **models.ForeignKey** 来实现，此处不再赘述。

- Django 模型层定义了一种更直接的 *M*∶*N* 关系建模方式，即在两个模型中的任意一个中定义 **models.ManyToManyField** 类型的字段，多对多关系的 Account 与 Contact 模型定义的如下：
  ```python
  from django.db import models 
  class Account(models.Model): 
      user_name = models.CharField(max_length = 80) 
      password = models.CharField(max_length = 255) 
      reg_date = models.DateField() 
      def __unicode__(self): 
      	return "Account: %s" % self.user_name 
      
  class Contact(models.Model): 
      accounts = models.ManyToManyField(
          Account
      ) 
      zip_code = models.CharField(max_length=10) 
      address = models.CharField(max_length=80) 
      mobile = models.CharField(max_length=20) 
      def __unicode__(self): 
      	return "%s, %s" % (self.accout.user_name, mobile)
  ```

  上述代码通过在 Contact 中定义引用 Acccount 的 ManyToManyField，实现了两个模型的多对多关联，对此模型定义的操作演示如下：
  ```python
  # 分别建立并保存 Account 和 Contact 对象
  >>> a1 = Account(user_name = "Leon") 
  >>> a1.save() 
  >>> c1 = Contact(mobile = "13912345003") 
  >>> c1.save() 
  
  >>> c1.accounts.add(a1) # 通过 Contact 对象建立关系
  
  >>> a2 = Account(user_name = "Terry") 
  >>> a2.save() 
  >>> a2.contact_set.add(c1) # 通过 Account 对象建立关系
  
  >>> a3 = Account(user_name = "Terry") 
  >>> a3.contact_set.add(c1) # 未保存过的对象不能与其他对象建立关系
  Traceback (most recent call last): 
  ... 
  ValueError: 'Account' instance needs to have a primary key value before a many-to-many relationship can be used. 
  
  >>> a1.contact_set.remove(c1) # 取消单个对象关联
  
  >>> a1.contact_set.clear() # 取消 a1 与所有其他 Contact 对象的关联
  ```

### 面向对象ORM

Django 模型层 ORM 的一个强大之处是对模型继承的支持，该技术将 Python 面向对象的编程方法与数据库面向关系表的数据结构有机地结合。Django 支持三种风格的模型继承。

- **抽象类继承：**父类继承自 models.Model，但不会在底层数据库中生成相应的数据表。父类的属性列存储在其子类的数据表中。
- **多表继承：**多表继承的每个模型类都在底层数据库中生成相应的数据表管理数据。
- **代理模型继承：**父类用于在底层数据库中管理数据表；而子类不定义数据列，只定义查询数据集的排序方式等元数据。

#### 1.抽象类继承

抽象类继承的作用是在多个表有若干相同的字段时，可以使开发者将这些字段统一定义在抽象基类中，免于重复定义这些字段。抽象基类的定义通过在模型的 Meta 中定义属性 **abstract = True** 来实现。抽象基类的举例如下：

```python
from django.db import models 

class MessageBase(models.Model): 
    id = models.AutoField() 
    content = models.CharField(max_length=100) 
    user_name = models.CharField(max_length=80) 
    pub_date = models.DateField() 
    class Meta: 
    	abstract = True # 定义本类为抽象基类
        
class Moment(MessageBase): 
    headline = models.CharField(max_length=50) 
    LEVELS = ( 
        ('1', 'Very good'), 
        ('2', 'Good'), 
        ('3', 'Normal'), 
        ('4', 'Bad'), 
    ) 
    
class Comment(MessageBase): 
    level = models.CharField(max_length=1, choices=LEVELS)
```

本例中定义了一个抽象基类 MessageBase，用于保存消息的 4 个公用字段：id、content、user_name、pub_date。子类 Moment 和 Comment 继承自 MessageBase，并分别定义了自己的一个字段。本例中的 **3 个类映射到数据库**后会被定义为**两个数据表**。

- 数据表 moment：有 id、content、user_name、pub_date、headline 5 个字段。
- 数据表 comment：有 id、content、user_name、pub_date、level 5 个字段。

在子类模型的编程中，可以直接引用父类定义的字段，比如：

```python
>>> m1 = Moment(user_name = "Terry", headline = "hello world") # 新建 Moment 对象
>>> m1.content = "reference parent field in subclass" 
>>> a1.save()
```

#### 2.多表继承

在多表继承技术中，无论是父表还是子表都会用数据库中相对应的数据表维护模型数据，父类中的字段不会重复地在多个子类的相关数据表中进行定义。从这种意义上讲，多表继承才是真正面向对象的 ORM 技术。

多表继承的定义不需要特殊的关键字。在 Django 内部通过在父模型和子模型之间建立一对一关系来实现多表继承技术。如下代码定义了 MessageBase 及其子类的多表继承版本：

```python
from django.db import models 
class MessageBase(models.Model): 
    id = models.AutoField() 
    content = models.CharField(max_length=100) 
    user_name = models.CharField(max_length=80) 
    pub_date = models.DateField() 
    
class Moment(MessageBase): 
    headline = models.CharField(max_length=50)
    
class Comment(MessageBase): 
    level = models.CharField(max_length=1, choices=LEVELS)
```

本例在数据库中会实际生成 3 个数据表。

- 数据表 MessageBase：有 id、content、user_name、pub_date 4 个字段。
- 数据表 Moment：有 id、headline 两个字段。
- 数据表 Comment：有 id、level 两个字段。

在对模型的编程过程中，子类仍然可以直接引用父类定义的字段；同时子类可以通过父类对象引用访问父类实例，比如：

```python
# 新建 Moment 对象，直接在子类中引用父类字段
>>> m1 = Moment(user_name = "Terry", headline = "hello world") 
>>> m1.content = "reference parent field in subclass" 
>>> a1.save() 

# 通过父类实例引用父类字段
>>> print(m1.messagebase.content) 
reference parent field in subclass
```

> 多表继承时，在子类实例中通过小写的父类名字可以引用父类的实例。

#### 3.代理模型继承

在前两种继承模型中子类模型都有实际存储数据的作用；而在代理模型继承中子类只用于管理父类的数据，而不实际存储数据。代理模型继承通过在**子类的 Meta 中定义 proxy=True** 属性来实现，举例如下：

```python
from django.db import models 
class Moment(models.Model): 
    id = models.AutoField() 
    headline = models.CharField(max_length=50) 
    content = models.CharField(max_length=100) 
    user_name = models.CharField(max_length=80) 
    pub_date = models.DateField() 
    
class OrderedMoment(Moment): 
    class Meta: 
        proxy = True 
        ordering = ["-pub_date"]
```

在本例中定义了父类模型 Moment 用于存储数据，而后定义了子类模型 OrderedMoment 用于管理根据 pub_date 倒序排列的 Moment。使用代理模型继承的原因是子类中新的特性不会影响父类模型及其已有代码的行为。

## Django视图层

Django 视图层的主要工作是衔接 HTTP 请求、Python 程序、HTML 模板等。

### URL映射

URL 分发（URL dispatcher）映射配置可以被看作 Django 项目的入口配置，通过 URL dispatcher 可以指定用户每一次访问的后台 Python 处理函数是什么。

#### 1.普通URL映射

每个 Django 项目都有一个 urls.py 文件用于维护 URL dispatcher，对该文件的内容举例如下：

```python
from django.urls import path, re_patrh as url 
from . import views

urlpatterns = [ 
    path(r'year/2018', views.moments_2018), 
    url(r'^year/([0-9]{4})/$', views.year_moments), 
    url(r'^month/([0-9]{4})/([0-9]{2})/$', views.month_moments), 
    url(r'^single/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.single), 
]
```

文件通过维护 urlpatterns 列表的元素完成 URL 映射，每个元素可以是一个django.urls.re_path()函数执行结果，也可以是 django.urls.path()函数结果。两个函数的第 1 个参数是 HTTP 路径，第 2 个参数是该路径被映射到的 Python 函数名；它们的区别在于 re_path()函数的HTTP 路径名是正则表达式，而 path()函数的 HTTP 路径是普通字符串。

本例中维护了 4 个 URL 映射，解析如下。

- 第 1 个路径是一个严格路径，即只匹配“year/2018”。该路径调用的是 views.py 文件中的 moments_2018()函数，调用的形式是：
  ```python
  moments_2018(request)
  ```

  其中的 request 是用户请求对象。

- 函数re_path()的路径用正则表达式定义，其中的“^”意为“以……开始”，“$”意为“以……结束”。第 2 个 url()匹配的路径是任何“year/××××”路径，其中要求××××是四位数字。其调用函数是 views.py 中的 year_moments，并且会把四位数字作为变量传给该函数，调用参数的形式是 year_moments(request, ××××)。

- 第 3 个和第 4 个 url()的解析方式与第 2 个 url()类似，只是有更多的路径变量，调用方式分别是 month_moments(request, ××××, yy)和 single(request, ××××, yy, zz)。

  > 注意：函数 url()中的路径名不包含网站的主机名，比如用户访问的 URL 形式可能是http://××.××.××.××/year/2018/02，该地址将直接匹配本例的第 3 个映射。

#### 2.正则表达式

#### 3.命名URL参数映射

在普通 URL 映射中，Django 将 URL 中的变量参数按照路径中的出现顺序传递给被调用函数。而命名 URL 参数映射使得开发者可以定义这些被传递参数的参数名称，命名 URL 参数的定义方式是“?P<param_name>pattern”，举例如下：

```python
from django.urls import re_path as url 
from . import views 
urlpatterns = [ 
    url(r'^year/2018/$', views.moments_2018), 
    url(r'^year/?P<year>([0-9]{4})/$', views.year_moments), 
    url(r'^month/?P<year>([0-9]{4})/?P<month>([0-9]{2})/$', views.month_moments), 
]
```

本例中的后两个 url()使用命名参数进行定义，它们调用 views.py 中的 Python 函数，调用方式分别为：year_moments(request, year = xxxx) 和 month_moments(request, year = xxxx, month =xx)。

> 注意：当多个 URL 映射定义可以匹配同一个 URL 地址时，Django 会选取在 urlpatterns列表中的第 1 个匹配的元素。比如 URL“year/2018”可以同时匹配第 1 个和第2 个映射，但 Django 会对针对该地址的访问调用函数 moments_2018()。

#### 4.分布式URL映射

在大型 Django 项目中，一个项目可能包含多个 Django 应用，而每个应用都有自己的 URL映射规则。这时将所有的 URL 映射都保存在一个 urls.py 文件中就不利于对网站的维护，所以Django 用 include()函数提供了分布式 URL 映射的功能，使得 URL 映射可以被编写在多个 urls.py文件中。在项目根映射文件 djangosite/djangosite/urls.py 中引用其他 URL 映射文件的示例代码如下：

**父文件**

```python
from django.urls import include, re_path as url 
urlpatterns = [ 
    url(r'^moments/', include('djangosite.app.urls')), 
    url(r'^admin/', include('djangosite.admin.urls')), 
]
```

两组 url()函数进行了映射定义。

- 以 moments/开头的 URL 被转接到 djangosite.app.urls 包中，即 djangosite/app/urls.py 文件。
- 以 admins/开头的 URL 被转接到 djangosite.admin.urls 包中，即 djangosite/admin/urls.py文件。

被包含的子映射文件 djangosite/app/urls.py 的示例如下：

**子文件**

```python
from django.urls import include, re_path as url 
urlpatterns = [ 
    url(r'^year/?P<year>([0-9]{4})/$', views.year_moments), 
    url(r'^admin/', include('djangosite.admin.urls')), 
]
```

子映射文件的 urlpatterns 中可以包含普通的 URL 映射元素，也可以用 include()引用其他urls.py 文件。对这两个文件的映射结果说明如下。

- 由于子文件中的第 1 行 url()配置，对 http://xx.xx.xx.xx/moments/year/2013 的访问会定位到 djangosite/app/views.py 中的 year_moments()函数。
- 由于子文件中的第 2 行 url()配置，对 http://xx.xx.xx.xx/moments/admin 的访问会转到djangosite/admin/urls.py 文件进行解析。
- 由于父文件中的第 2 行 url() 配置，对 http://xx.xx.xx.xx/admin 的访问会转到djangosite/admin/urls.py 文件进行解析。
- 因为在父 urls.py 中没有配置过，所以对 http://xx.xx.xx.xx/year/2013 的访问将找不到任何映射。

#### 5.方向解析

除了上述从 HTTP URL 映射到 Python 视图函数的丰富的映射功能，Django 还提供了反向的从映射名到 URL 地址的解析功能。URL 反向解析使得开发者可以用映射名代替很多需要写绝对 URL 路径的地方，提高了代码的可维护性。

Django 的 URL 反向解析功能在模板文件和 Python 程序中有不同的调用方法：在模板文件中用{%url %}标签调用反向解析；在 Python 程序中用 django.urls.reverse()函数调用反向解析。下面举例说明，首先定义 URL 映射规则如下：

```python
from django.urls import re_path as url, include

urlpatterns = [ 
    url(r'^year/2018/$', views.year_moments, name = "moments_2018"), 
]
```

其中定义了一个 URL 映射，并通过 name 参数将该映射命名为 moments_2018。在需要获得该 URL 的模板文件中可以通过{%url %}标签进行声明，比如：

```html
<a href="{% url 'moments_2018' %}"> 
    查看 2018 年消息
</a>
```

其中用映射名“moments_2018”作为反向解析的参数，该模板解析后的结果为：

```html
<a href="/year/2018/"> 
    查看 2018 年消息
</a>
```

而在 Python 代码与模板文件中的反向解析调用方式是使用 reverse()函数，比如views.py：

```python
from django.urls import reverse 
from django.http import HttpResponseRedirect 

def redirect_to_year_2018(request): 
    return HttpResponseRedirect(reverse('moments_2018')) 
```

#### 6.带参数的反向解析

反向解析还可以支持在 URL 路径和被调用函数中有参数的情况，比如对于带参数的映射：

```python
from django.urls import include, re_path as url 
urlpatterns = [ 
    url(r'^year/?P<year>([0-9]{4})/$', views.year_moments, name = "moments"), 
]
```

在模板文件的反向解析中，可以直接在{%url %}标签中添加参数，比如：

```html
<a href="{% url 'moments', 2017 %}">
    查看2017年消息
</a>
```

其中用映射名“moments”和 URL 参数 2017 作为反向解析的参数，该模板解析后的结果如下：

```html
<a href="/year/2017/"> 
    查看 2017 年消息
</a>
```

Python 代码中带参数的 URL 反向解析的调用方式举例如下：

```python
from django.urls import reverse 
from django.http import HttpResponseRedirect 

def redirect_to_year_2018(request): 
    return HttpResponseRedirect(reverse('moments', args=(2018,)))

# 其中 reverse()函数的 args 参数用于设置反向映射的 URL 参数
```

### 视图函数

视图函数是 Django 开发者处理 HTTP 请求的 Python 函数。在通常情况下，视图函数的功能是通过模型层对象处理数据，然后用如下方式中的一种返回 HTTP Response。

- 直接构造 HTTP Body。
- 用数据渲染 HTML 模板文件。
- 如果有逻辑错误，则返回 HTTP 错误或其他状态。

#### 1.直接构造HTML页面

对于一些简单的页面，可以直接在视图函数中构造返回给客户端的字符串，通过HttpResponse()函数封装后返回。如下例子为返回当前服务器的时间给客户端：

```python
from django.http import HttpResponse 
import datetime 

def current_datetime(request): 
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    return HttpResponse(now)
```

#### 2.用数据渲染HTML模版文件

由于模板文件可以包含丰富的 HTML 内容，因此使用渲染模板文件的方法返回页面是最常用的一种 Django 视图函数技术。模板渲染通过 render()函数实现，举例如下：

```python
from django.shortcuts import render 
from app.models import Moment 

def detail(request, moment_id): 
    m = Moment.objects.get(id=moment_id) 
    return render(request, 'templates/moment.html',{'headline': m.headline, 'user': m.user_name})
```

函数 render()的第 1 个参数是 HTTP request，第 2 个参数是模板文件名，第 3 个参数是以字典形式表达的模板参数。

#### 3.返回HTTP错误

HTTP 错误通过 HTTP 头中的 Status 表达，通过给 HttpResponse 构造函数传递 status 参数，可以返回 HTTP 错误或状态。比如：

```python
from django.http import HttpResponse 
def my_view(request): 
    return HttpResponse(status=404)
```

通过上述代码可返回 HTTP 404 错误，即“Page Not Found”。为了方便开发者，Django 对于常用的 Status 状态定义了若干 HttpResponse 的子类，开发者需要返回非 200 OK 状态时，也可直接通过这些子类定义 Response，比如下面是用 HttpResponseNotFound 子类的实例返回 404错误：

```python
from django.http import HttpResponseNotFound 
def my_view(request): 
    return HttpResponseNotFound()
```

其他一些常用的特定状态 HttpResponse 子类如下。

- HttpResponseRedirect：返回 Status 302，用于 URL 重定向，需要将重定向的目标地址作为参数传给该类。

  > HttpResponseRedirect 的参数经常使用 URL 反向映射函数 reverse()获得，这样可以避免在更改网站 urls.py 内容的时候维护视图函数中的代码。

- HttpResponseNotModified：返回 Status 304，用于指示浏览器用其上次请求时的缓存结果作为页面内容显示

- HttpResponsePermanentRedirect：返回 Status 301，与 HttpResponseRedirect 类似，但是告诉浏览器这是一个永久重定向。

- HttpResponseBadRequest：返回 Status 400，请求内容错误。

- HttpResponseForbidden：返回 Status 403，禁止访问错误。

- HttpResponseNotAllowed：返回 Status 405，用不允许的方法（Get、Post、Head 等）访问本页面。

- HttpResponseServerError：返回 Status 500，服务器内部错误，比如无法处理的异常等。

### 模版语法

模板文件是一种文本文件，模板文件主要由目标文件的内容组成（比如 HTML、CSS 等），辅以模板的特殊语法用于替换动态内容。下面是一个功能较全的典型模板文件：

```html
{% extends "base.html" %} 

{% block title %}{{ section.title }}{% endblock %} {# 块内容，用于模板继承#} 

{% block content %} {# 块内容，用于模板继承#} 

<h1>{{ section.title }}</h1> {# 变量替换#} 

{% for moment in moment_list %} {# 流程控制——for 循环#} 

<h2> 
	{{ moment.headline|upper }} {# 带过滤器的变量替换#} 
</h2> 

{% endfor %} 
{% endblock %}

<!--其中大括号{}包含的内容均为模板文件的特殊语法，其中{# #}之间的内容为模板的注释内容。-->
```

#### 1.变量替换

用双大括号标记{{ variable }} 指示进行变量内容替换，只需在其中写入变量名即可，比如：`{{ moment.headline }} `，其中的 moment 是在视图函数渲染模板时传递给 render()函数的参数之一。

#### 2.过滤器

过滤器（filter）在模板中是放在变量后并用于控制变量显示格式的技术。变量与过滤器之间通过管道符号“|”连接，如下代码将 upper 过滤器应用在 moment.headline 变量中：`{{ moment.headline | upper}} ` 其作用是指定以大写方式输出 moment.headline。

Django 中常用的其他过滤器如下:

- **add**：给 value 加上一个数值，比如{{ 123|add:"5" }}返回 128。

- **addslashes**：单引号加上转义号。

- **capfirst**：第 1 个字母大写，比如{{ "good"|capfirst }}返回 Good。

- **center**：输出指定长度的字符串，把变量居中，比如{{ "abcd"|center:"50" }}。

- **cut**：删除指定字符串，比如{{ "You are not a Englishman"|cut:"not" }}。

- **date**：格式化日期。

- **default**：如果值不存在，则使用默认值代替，比如{{ value|default:"(N/A)" }} 。

- **default_if_none**：如果值为 None，则使用默认值代替，使用方式与 default 类似。

- **dictsort**：按某字段排序，变量必须是一个 dictionary。

  ```html
  {% for moment in moments|dictsort:"id" %} 
      * {{ moment.headline }} 
  {% endfor %}
  ```

  如上代码指定 moments 用 id 字段排序后逐一进行 headline 输出。

- **dictsortreversed**：按某字段倒序排序，变量必须是一个 dictionary。

- **divisibleby**：判断是否可以被某数字整除。

- **escape**：按 HTML 转意，比如将“<”转换为“<”，将“>”转换为“>”。

- **filesizeformat**：增加数字的可读性，转换结果为 13KB、89MB、3 Bytes 等。

- **first**：返回列表的第 1 个元素，变量必须是一个列表，比如{{['English', 'Chinese', 'Japanese'] | first}}。

- **floatformat**：转换为指定精度的小数，默认保留 1 位小数。

  ```html
  {{ 34.23234|floatformat }} {#返回 34.2 #} 
  {{ 34.23234|floatformat:3 }} {#返回 34.232 #}
  {{ 34.23234|floatformat:4 }} {{#返回 34.2323 #}
  ```

- **get_digit**：从个位数开始截取指定位置的数字，比如{{ 23456 |get_digit:"1" }}返回 6。

- **join**：用指定分隔符连接列表，比如{{ ['abc', '45']|join:"*" }}返回 abc*45。

- **length**：返回列表中元素的个数或字符串的长度。

- **length_is**：检查列表、字符串的长度是否符合指定的值，比如{{ "hello"|length_is:"3" }}返回 False。

- **linebreaks**：用\<p>或\<br/>标记包裹变量，其中单独的换行被替换为\<br/>，空行前后被分割为\<p>。

  ```html
  {{"Hi\n\nDavid"|linebreaks }} {#返回 "<p>Hi</p> <p>David</p>" #}
  ```

- **linebreaksbr**：用\<br/>标记代替换行符。

- **linenumbers**：为变量中的每一行加上行号。

- **ljust**：输出指定长度的字符串，变量左对齐，比如{{"ab"|ljust:5}}返回"ab "。

- **lower**：字符串变换为小写，比如{{ "ABCD"|lower }}。

- **make_list**：将字符串转换为列表，比如 {{"abc" | make_list }}返回['a', 'b', 'c']。

- **pluralize**：根据数字确定是否输出英文复数符号。

  ```html
  You have {{ num_messages }} message{{ num_messages|pluralize }}.
  ```

  该过滤器将在 num_messages 大于 1 的时候输出英文复数符号 s。

- **random**：返回列表的随机一项。

- **removetags**：删除字符串中指定的 HTML 标记。

  ```html
  {{ value|removetags:"h1 h2" }} 
  当 value 是"<h1>Good morning</h1> <h3>David</h3>"时，该过滤器的输出为"Good morning <h3>David</h3>"。
  ```

- **rjust**：输出指定长度的字符串，变量右对齐。

- **slice**：切片操作，即返回列表、字符串的一部分，比如{{[3, 9, 1] | slice: ":2"}}返回[3, 9]。

- **slugify**：在字符串中留下减号和下画线，其他符号删除，空格用减号替换。

- **stringformat**：字符串格式化，使用 Python 的字符串格式的语法。

- **time**：返回日期的时间部分。

- **timesince**：以“到现在为止过了多长时间”的形式显示时间变量，可能的结果格式如 45 days、3 hours 等。

- **timeuntil**：与 timesince 类似，但是比较的是当前时间与之后的某个时间。

- **title**：每个单词的首字母大写。

- **truncatewords**：将字符串转换为省略表达方式，传入参数表达保留的单词个数，比如{{ "This is a lovely cat"|truncatewords:"3" }}返回“This is a …”。

- **truncatewords_html**：与 trancatewords 类似，但保留其中的 HTML 标签，比如{{ "\<p>This is a lovely cat\</p>"|truncatewords:"3" }}返回“\<p>This is a …\</p>”。

- **upper**：转换为全部大写形式。

- **urlencode**：将字符串中的特殊字符转换为 URL 兼容表达方式。

  ```html
  {{"https://www.example.org/foo?a=b&c=d" | urlencode}}
  ```

  返回“https%3A//www.example.org/foo%3Fa%3Db%26c%3Dd”

- **urlize**：将变量字符串中的 URL 由纯文本变为可单击的链接。

  ```html
  {{"点击 www.django.com" | urlize}}
  ```

  返回“点击<a href="http://www.django.com" rel="nofollow">www.django.com</a>”。

- **wordcount**：返回变量字符串中的单词数。

- **yesno**：将布尔变量变换为字符串 yes、no 或 maybe，也可以在参数中指定变换的结果。

  ```html
  {{ true|yesno:"Yes,No,Perhaps" }} {#返回 Yes #} 
  {{ false|yesno }} {#返回 no #} 
  {{ None|yesno:"Yes,No,Perhaps" }} {#返回 Perhaps #}
  ```

#### 3.流程控制

Django 模板提供基本的流程控制功能，包括用{% for %}语句实现的循环逻辑和用{% if %}语句实现的判断逻辑。for 语句的示例代码为：

```html
{% for moment in moment_list %} {# 流程控制——for 循环#} 
<h2> 
    {{ moment.headline|upper }} {# 带过滤器的变量替换#} 
</h2> 
{% endfor %}
```

上述代码中 moment_list 是视图文件传给模板渲染函数 render()的列表参数，for 语句针对moment_list 中的每个元素生成一个\<h2>\</h2>标签，用于显示 moment 的 headline 成员。

与其他高级语言中的 if 语句类似，Django 模板也提供了 if 语句的 elif、else 等子语句，一个 if 及其子语句的完整演示代码如下：

```html
{% if moment.id < 10 %} 
    <h1> {{ moment.headline }} </h1> 
{% elif moment.id < 20 %} 
    <h2> {{ moment.headline }} </h2> 
{% else %} 
     <p> {{ moment.headline }} </p> 
{% endif %}
```

该语句根据 moment.id 的大小用不同的格式输出 moment.headline。

#### 4.模版继承

模板继承功能使得页面设计者可以将多个页面的公用部分编写在一个模板文件中，然后在其他模板文件中共享该公用部分的内容。根据共享文件之间的关系，可以将模板文件分为两种类型。

- 父模板文件：保存公用部分的内容，同时指定页面的整体框架，父模板文件一般包括页面头、导航栏、页脚、ICP 声明等。
- 子模板文件：用于扩展父模板文件，在其中编写每个页面自身的特有内容。

父模板文件的内容示例如下：

```html
<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <link rel="stylesheet" href="style.css" /> 
    <title>{% block title %}My django site{% endblock %}</title> 
</head> 
<body> 
    <div id="sidebar"> 
        {% block sidebar %} 
            Need to add Navigator here 
        {% endblock %} 
    </div> 
    <div id="content"> 
        {% block content %} 
        {% endblock %} 
    </div> 
</body>
</html>
```

父文件的主要内容是定义了页面的框架，同时用{%block block_name%}…{% endblock %}块定义可以被子文件覆盖、重写的内容。将该父文件命名为 base.html，扩展该父文件的子模板文件如下：

```html
{% extends "base.html" %} 

{% block title %}My moment site{% endblock %} 

{% block content %} 
Here is child file content that will show in result. 
{% endblock %} 

{% block new_block %} 
Here is child file content that will not show in result. 
{% endblock %}
```

子文件中通过{%extends %}标签指定父模板文件，然后通过{%block %}块重写需要覆盖的父文件中的内容。视图函数渲染子文件的结果如下：

```html
<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <link rel="stylesheet" href="style.css" /> 
    <title>My moment site</title> 
</head> 
<body> 
    <div id="sidebar"> 
    	Need to add Navigator here 
    </div> 
    <div id="content"> 
    	Here is child file content that will show in result. 
    </div> 
</body> 
</html>
```

## Django表单

### 表单绑定状态

Django 为继承自 Form 类的表单维护了一个绑定（bound）状态。

- 如果一个表单对象在实例化后被赋予过数据内容，则称该表单处于 bound 状态。只有处于 bound 状态的表单才具有表单数据验证（validate data）的功能。
- 如果未被赋予过数据内容，则表单处于 unbound 状态。只有处于 unbound 状态的表单才能被赋予数据，使该表单变为 bound 状态。

> 注意：已经处于 bound 状态的表单不能在 Python 代码中修改其数据，而只能由网页用户在页面中输入数据进行修改。

通过 Form 的 is_bound 属性检查表单状态

```python
>>> f = MomentForm() 
>>> print(f.is_bound) 
False 
>>> f = MomentForm({'headline': 'hello'}) 
>>> print(f.is_bound) 
True
```

### 表单数据验证

Django 表单数据验证是指在服务器端用 Python 代码验证表单中数据的合法性。表单验证分为如下两类。

- 字段属性验证：验证表单中的字段是否符合特定的格式要求，比如 CharField 字段是否满足了 max_length 要求、非空字段是否已经赋值等。
- 自定义逻辑验证：验证开发者自定义的一些逻辑要求，比如 moment 的 content 长度必须比 headline 长、不能包含某些关键字等。

#### 1.字段属性验证

字段属性验证要求通过 model 中字段的约束完成，在 Form 渲染的过程中 Django 会自动根据验证约束要求验证字段内容，如果字段不符合要求，则会自动显示错误信息并提示用户。

开发者还可以用 is_valid()函数在代码中获得表单验证是否通过的信息，用 errors属性获得错误提示信息，比如：

```python
>>> f = MomentForm({'user_name':'David'}) 
>>> print(f.is_valid()) 
False 

>>> print(f.error) 
{'content': ['This field is required.']}
```

由于在 MomentForm 的初始化中只设置了 user_name 的值，而没有设置不能为空的 content的值，因此此时调用表单的 is_valid()结果为 False。表单 is_valid()函数通常在视图函数的开发中起重要的作用。下面是典型的表单视图函数的设计结构：

```python
def viewer(request): 
    if request.method == 'POST': 
    	form = XXXForm(request.POST) 
        if form.is_valid(): 
            # 此处编写正常的表单提交的业务逻辑
            # 处理完成后用 redirect 重定向页面
        else: 
            # 此处编写提交数据不完全的业务逻辑，比如显示特定的错误信息等
```

#### 2.自定义逻辑验证

如果开发者需要在Django进行表数据验证时判断自定义的复杂逻辑，则可以通过重载 Form子类的 clean()函数进行定义。修改 MomentForm 的定义如下：

```python
from django.forms import ModelForm, ValidationError 
from app.models import Moment 

class MomentForm(ModelForm): 
    class Meta: 
        model = Moment 
        fields = '__all__' 
        
    def clean(self): 
        cleaned_data = super(MomentForm, self).clean() 
        content = cleaned_data.get("content") 
        if content is None: 
        	raise ValidationError( "请输入 Content 内容!") 
        elif content.find("ABCD")>=0: 
        	raise ValidationError( "不能输入敏感字 ABCD !" ) 
        return cleaned_data
```

在 MomentForm 中增加了对 clean()函数的定义，该函数在开发者调用 Form.is_valid()函数时自动被 Django 调用，开发者应该将针对表单的自定义验证逻辑写在 clean()函数中。如果验证检测到逻辑错误，则通过抛出 ValidationError()异常结束本次验证；如果验证数据正确，则返回从基类中得到的 cleaned_data。

### 检查变更字段

当视图函数收到表单的 Post 提交时，经常需要通过验证用户是否修改了表单数据然后进行相应的处理。Django 提供了表单函数 has_changed()来判断用户是否修改过表单数据，使用方法如下：

```python
def view_moment(request) 
    data = {
        'content': 'Please input the content', 
        'user_name': '匿名', 
        'kind':'Python 技术'
    } 
    f = MomentForm(request.POST, initial=data) 
    if f.has_changed(): 
    # 在此处编写保存 f 的代码
        print("如下字段进行了修改: %s" % ") 
        for field in f.changed_data: 
        	print(field)
```

在初始化 Form 实例时要传入如下两个参数：

- reqeust.POST：Django 从其中解析出用户的输入数据。
- initial：Form 的初始值，在调用 has_changed 时，Django 用 initial 中的字段值与初始值相比较，如果有变化则返回 True。

Django 不仅能够判断是否有字段修改过，还能用 changed_data 属性精确定位用户对哪些字段进行了修改。changed_data 是包含字段名的列表

## 个性化管理员站点

### 模型

通过定义继承自 django.contrib.admin.ModelAdmin 的子类，可以定制个性化的数据模型管理功能，并且需要在应用的 admin.py 文件中注册模型类时指定该子类，示例如下：

```python
from django.contrib import admin 
from myproject.myapp.models import Author 

class MomentAdmin(admin.ModelAdmin): 
	empty_value_display = "空值" 
admin.site.register(Moment,MomentAdmin)
```

本例中定义了一个数据模型管理类 MomentAdmin，并用 admin.site.register()函数指定其作为模型 Moment 的管理类。MomentAdmin 中用属性 empty_value_display 定义了模型管理界面中对空值的显示方式，这些个性化的管理功能还包括指定模型中的哪些字段可以被管理及每页显示的模型实例数量等。对常用的管理类属性描述如下:

- **date_hierarchy**：设置一个日期类型字段，使其出现在按日期导航找模型实例的界面中。

- **empty_value_display**：设置一个字符串，定义空值的显示方式。除了在表级别指定空值显示的方式，还可以按字段配置，比如：

  ```python
  class MomentAdmin(admin.ModelAdmin): 
      empty_value_display = "空值" 
      headline. empty_value_display = "未设标题"
  ```

  本例中将表中默认的空值显示方式设置为“空值”，同时设置 headline 字段的空值显示为“未设标题”。

- **fields和exclude**：分别用于设置需要管理的字段和排除管理的字段。对如下模型Moment来说：

  ```python
  class Moment(models.Model): 
      content = models.CharField(max_length=300, null=False) 
      user_name = models.CharField(max_length = 20, default = '匿名') 
      kind = models.CharField(max_length = 20, choices = KIND_CHOICES, default= KIND_CHOICES[0])
  ```

  下面的两个管理类（MomentAdmin1 和 MomentAdmin2）有相同的作用，都是设定管理界面只管理 content 和 kind 字段
  ```python
  from django.contrib import admin 
  class MomentAdmin1(admin.ModelAdmin): 
      fields = ('content', 'kind') 
      
  class MomentAdmin2(admin.ModelAdmin): 
      exclude = ('user_name',)
  ```

- **fieldsets**：配置字段分组，可以美化管理界面的模型配置界面。如下代码将 Moment的字段分为两个组：

  ```python
  from django.contrib import admin 
  # Register your models here. 
  from .models import Moment 
  class MomentAdmin(admin.ModelAdmin): 
      fieldsets = ( 
          ("消息内容", { 
          'fields': ('content', 'kind') 
          }), 
          ('用户信息', { 
          'fields': ('user_name',), 
          }), 
      ) 
  admin.site.register(Moment, MomentAdmin)
  ```

  这样，在编辑 Moment 对象时，管理界面会把字段分为两组显示

- **list_editable**：设置字段列表，指定模型中的哪些字段可以编辑。如果设置了本属性，则没有在本属性中定义的字段将不能在管理界面中编辑。

- **list_per_page**：设置一个整数，指定每页显示的实例数量，默认为 100。

- **search_fields**：设置字段列表，出现一个搜索页面使管理员能够按照这些字段进行实例搜索。

- **ordering**：设置字段列表，定义管理页面中模型实例的排序方式。

### 模板

如果读者需要在管理站点页面中增加独特的显示内容，则可以通过继承管理站点的默认模板文件进行开发。

假设 Django 被安装在虚环境 venv 中，则 Django 的默认管理站点的模板文件都被保存在如下路径中：

```shell
# cd venv/lib/python3.7/site-packages/django/contrib/admin/templates/admin
```

其中包含了所有默认管理站点所使用的模板文件，它们是：

```shell
# ls venv/lib/python3.7/site-packages/django/contrib/admin/templates/admin 
```

开发者可以继承它们中的任意文件，以定制自己的管理站点页面。

节以重载登录页面login.html 为例演示 Django 管理模板文件的定制技术

#### 1.定义子模板文件路径

在项目目录中按如下路径生成子模板文件 login.html：

```shell
djangosite/ 			//项目根目录
 manage.py 
 djangosite/ 			//项目文件目录
 app/ 					//应用目录
 templates/ 			//新生成的模板文件目录
 	admin/ 
 	index.html
```

#### 2.修改项目setting.py

打开文件 djangosite/djangosite/settings.py, 配置其中的 TEMPLATES 的 DIRS 项目，将新生成的模板文件路径加入其中，比如：

```django
TEMPLATES = [ 
    { 
    'BACKEND': 'django.template.backends.django.DjangoTemplates', 
    'DIRS': [os.path.join(BASE_DIR,'templates')], # 本行中的路径为新加项
    'APP_DIRS': True, 
    'OPTIONS': { 
        'context_processors': [ 
            'django.template.context_processors.debug', 
            'django.template.context_processors.request', 
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages', 
        	],
		}, 
	}, 
]
```

#### 3.开发子模板文件

打开 Django 默认的 login.html，检查其中可继承的 block，并在子模板文件中改写其内容以达到定制目的。读者打开默认的 login.html 文件后，可以发现其中有很多可改写项，比如content_title、bodyclass、nav-global 等，如下子模板文件可改写 content_tilte 块的内容：
```html
{% extends "admin/login.html" %} 
{% block content_title %} 
欢迎登录 Djangosite 的管理网站
{% endblock %}
```

#### 4.测试定制效果

至此已完成管理模板的定制开发工作，此时可以打开管理网站，

### 站点

如果需要修改一些管理站点中的通用属性，比如管理站点头、站点标题等，则可以通过定义自己的 AdminSite 类来实现。

#### 1.定义AdminSite子类

自定义的 AdminSite 需要放在应用的 admin.py 文件中，打开 djangosite/app/admin.py 文件，添加如下代码：
```python
from django.contrib import admin 
class MyAdminSite(admin.AdminSite): # 定义 AdminSite 子类
    site_header = '我的管理网站' # 配置自定义的属性
    
admin_site = MyAdminSite() # 实例化一个子类
admin_site.register(Moment, MomentAdmin) # 用子类实例注册需要管理的模型类
```

#### 2.修改项目urls.py

在 djangosite/djangosite/urls.py 文件的 urlpatterns 列表中配置用 admin_site 定义的管理站点URL 映射，比如：

```python
from django.conf.urls import url, include 
from django.contrib import admin 
from app.admin import admin_site 
urlpatterns = [ 
    url(r'^admin/', admin_site.urls), # 修改本行
    url(r'^app/', include('app.urls')), 
]
# 用 admin_site.urls 替换了原来的 url.admin.urls
```

#### 3.测试定制效果

再次打开网站的 admin 登录页面，新的 AdminSite 定制效果

#### 4.AdminSite中常用的定制属性

- **site_header**：每个管理网页的页头都会出现的标题，即在 HTML 标签\<h1>中显示的内容。
- **site_title**：每个管理网页在浏览器窗口栏显示的页面名称，即 HTML 标签\<title>中显示的内容。
- **site_url**：管理站中 View site 按钮的目标地址，默认是网站根目录“\”。
- **login_form**：登录页面使用的 AuthenticationForm 子类名。









































