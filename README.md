django-stampu
=============

![django-stampu](http://cdn.fmartingr.com/github/django-stampu.png)

Convert your django sites into pure static content.

## Usage

1) Install django-stampu

```
pip install django-stampu
```

2) Add it to your `INSTALLED_APPS`

```
# ...
INSTALLED_APPS = (
    # ...
    'stampu',
)
```

3) Convert your site!

```
python manage.py stamp
```

Your static site will be on the `_static` folder.
