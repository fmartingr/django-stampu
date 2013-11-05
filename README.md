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

Your static site will be on the `_static` folder by default.

## Configuration

You can use two variabes on your `settings.py` to configure stampu's behaviour:

**STAMPU_CLEAN_START** default to `True` will remove the previous static folder and files before rendering again (if any).

**STAMPU_FOLDER** default to `_static` is the folder your rendered site will be saved into.
