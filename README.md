# drofji_automatically_django_admin

**drofji Automatically Django Admin** is a Django package designed to speed up admin panel prototyping. It automatically generates admin sections based on Django models using custom base classes and fields. Simply inherit your models from the `AutoAdminModel` base class, and the admin interface will be configured automatically.

## Features

- Automatic creation of `ModelAdmin` for all models inheriting from `AutoAdminModel`.
- Dynamic `list_display`, `search_fields`, and `list_filter` based on field flags.
- Supports custom filters: `DateRangeFilter` and `NumericRangeFilter` (requires `django-admin-rangefilter`).
- Custom ID formatting with leading zeros and semi-transparent style.
- Automatic inclusion of CSS and JS for enhanced admin visuals.

## Installation

Install via pip:

```bash
pip install drofji_automatically_django_admin
```

## Installation

### From PyPI

Install the stable release from PyPI:

```bash
pip install drofji_automatically_django_admin
```

### From GitHub

Install the latest version from the main branch:

```bash
pip install git+https://github.com/drofji/drofji-automatically-django-admin.git
```

Install a specific release (e.g., v1.0.0):

```bash
pip install git+https://github.com/drofji/drofji-automatically-django-admin.git@v1.0.0
```
## Django Setup

Add the following apps to your `INSTALLED_APPS` in `settings.py` (order matters):

- `admin_interface`, `colorfield` (before `django.contrib.admin`)  
- `django.contrib.*`  
- `rangefilter`, `drofji_automatically_django_admin` (after `django.contrib.*`)  
- Your apps, e.g., `example_app`

## Usage

1. Inherit your models from `AutoAdminModel`:

```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from drofji_automatically_django_admin import drofji_models, drofji_fields

class Customer(drofji_models.AutoAdminModel):
    name = drofji_fields.AutoAdminCharField(max_length=200, show_in_list=True, searchable=True, , verbose_name=_("Name"))
    email = drofji_fields.AutoAdminEmailField(show_in_list=True, searchable=True, verbose_name=_("Email"))
    age = drofji_fields.AutoAdminIntegerField(filterable=True, verbose_name=_("Age"))
```

2. Admin sections will be automatically registered with list display, search, and filters.  
3. IDs are formatted with leading zeros and styled automatically.  

### Overriding Admin Methods

You can override any `ModelAdmin` attribute or method directly from your model using `admin_overrides`:

```python
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from drofji_automatically_django_admin import drofji_models, drofji_fields

class Customer(drofji_models.AutoAdminModel):
    name = drofji_fields.AutoAdminCharField(max_length=200, verbose_name=_("Name"))

    # Custom display method for admin
    @admin.display(description=_("Name (Bold)"))
    def bold_name(self, obj):
        return format_html("<b>{}</b>", obj.name)

    # Admin overrides
    admin_overrides = {
        "bold_name": bold_name,  # Add custom method
        "list_display": ["formatted_id", "bold_name"]  # Override list_display
    }
```

- This allows you to customize the admin without manually creating a separate `ModelAdmin` class.  
- Works for methods like `get_queryset`, `save_model`, permissions, and any other `ModelAdmin` attributes.

## Recommendations

- Always add `admin_interface` and `colorfield` before `django.contrib.admin`.  
- Add `rangefilter` and `drofji_automatically_django_admin` after `django.contrib.*`.  
- Inherit your models from `AutoAdminModel` for full automation.  

## Links

- [drofji Automatically Django Admin (PyPI)](https://pypi.org/project/drofji-automatically-django-admin/)  
- [drofji Automatically Django Admin (GitHub)](https://github.com/drofji/drofji-automatically-django-admin)  
- [Django Docs](https://docs.djangoproject.com/en/stable/)  
- [django-admin-rangefilter (GitHub)](https://github.com/romgar/django-admin-rangefilter)  
- [django-admin-interface (GitHub)](https://github.com/fabiocaccamo/django-admin-interface)  
- [django-colorfield (GitHub)](https://github.com/fabiocaccamo/django-colorfield)