# Readable URLs
#### For cyrillic support:
 
```bash
$ sudo pip install unidecode
```

#### To model add:
```python
slug = models.SlugField(default='')
```
```python
def save(self, *args, **kwargs):
    from unidecode import unidecode
    from django.template.defaultfilters import slugify
    
    self.slug = slugify(unidecode(self.title))
    super().save(*args, **kwargs)

def get_absolute_url(self):
    kwargs = {'slug': self.slug,
              'pk': self.pk}
    return reverse('detail', kwargs=kwargs)
```
#### Then run:
```bash
$ python manage.py makemigrations app
$ python manage.py migrate
```
#### urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>-<str:slug>/', views.PostDetail.as_view(), name='detail'),
]
```
