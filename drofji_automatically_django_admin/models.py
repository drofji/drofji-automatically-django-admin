# myapp/models.py

from django.db import models
from django.contrib import admin
from django.apps import apps
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Try to import django-admin-rangefilter for "from-to" filters
try:
    from rangefilter.filters import DateRangeFilter, NumericRangeFilter
    RANGEFILTER_AVAILABLE = True
except ImportError:
    RANGEFILTER_AVAILABLE = False

# ---------------------------------------------
#  ID formatter (HTML: faded zeros)
# ---------------------------------------------
@staticmethod
@admin.display(description="ID")
def formatted_id(obj):
    raw = f"{obj.id:06d}"

    # split leading zeros
    i = 0
    while i < len(raw) and raw[i] == "0":
        i += 1

    leading = raw[:i]
    number = raw[i:] or "0"

    html = f'<span class="faded-zeros">{leading}</span>{number}'
    return mark_safe(html)


# ---------------------------------------------
# Replaces "id" → "formatted_id" in admin list
# ---------------------------------------------
def get_list_display(self, request):
    base = list(super(self.__class__, self).get_list_display(request))

    # # do nothing if formatted_id already present
    # if "formatted_id" in base:
    #     return base
    #
    # # replace "id" with "formatted_id"
    # if "id" in base:
    #     base[base.index("id")] = "formatted_id"

    return base

# ===========================================================
# Base model with automatic admin registration
# ===========================================================

# ===========================================================================================
#                                      AutoAdminModel
# ===========================================================================================
class AutoAdminModel(models.Model):
    """
    Base model that automatically configures Django Admin based on AutoAdmin*Field flags.
    """
    admin_enabled = True

    class Meta:
        abstract = True

    # -------------------------------------------------------
    # Compute admin fields dynamically
    # -------------------------------------------------------
    @classmethod
    def get_admin_fields(cls):
        fields = [f for f in cls._meta.get_fields() if hasattr(f, "name")]

        # --- list_display
        list_display = [f.name for f in fields if getattr(f, "show_in_list", True)]

        # Admin formatting handled later by get_list_display()
        # (we do NOT replace id here)

        # --- search fields
        search_fields = [f.name for f in fields if getattr(f, "searchable", False)]

        # --- filters
        list_filter = []

        for f in fields:
            if not getattr(f, "filterable", False):
                continue

            if RANGEFILTER_AVAILABLE:
                from drofji_automatically_django_admin.fields import (
                    AutoAdminDateField,
                    AutoAdminDateTimeField,
                    AutoAdminIntegerField,
                    AutoAdminFloatField,
                    AutoAdminDecimalField,
                )

                if isinstance(f, (AutoAdminDateField, AutoAdminDateTimeField)):
                    list_filter.append((f.name, DateRangeFilter))

                elif isinstance(f, (AutoAdminIntegerField, AutoAdminFloatField, AutoAdminDecimalField)):
                    list_filter.append((f.name, NumericRangeFilter))

                else:
                    list_filter.append(f.name)
            else:
                list_filter.append(f.name)

        return list_display, search_fields, list_filter

    # -------------------------------------------------------
    # Register the model in admin
    # -------------------------------------------------------
    @classmethod
    def register_admin(cls):
        if not cls.admin_enabled:
            return

        # Get default admin fields from the model
        list_display, search_fields, list_filter = cls.get_admin_fields()

        # Base attributes for the dynamic ModelAdmin
        admin_attrs = {
            "list_display": list_display,
            "search_fields": search_fields,
            "list_filter": list_filter,
            "formatted_id": formatted_id,  # Custom ID formatting
            "get_list_display": get_list_display,  # Replace "id" with formatted_id
            "Media": type("Media", (), {
                "css": {"all": ("drofji_automatically_django_admin/admin.css",)},
                "js": ("drofji_automatically_django_admin/admin.js",)
            })  # Include custom CSS/JS for admin
        }

        # -------------------------------------------------
        # Apply model-defined admin overrides
        # admin_overrides = { "method_or_attr_name": callable_or_value }
        # -------------------------------------------------
        overrides = getattr(cls, "admin_overrides", {})
        for name, value in overrides.items():
            admin_attrs[name] = value

        # Create a dynamic ModelAdmin class
        admin_class = type(
            f"{cls.__name__}Admin",
            (admin.ModelAdmin,),
            admin_attrs
        )

        # Register the model with Django admin
        try:
            admin.site.register(cls, admin_class)
        except admin.sites.AlreadyRegistered:
            pass

    # -------------------------------------------------------
    # Register all AutoAdminModel children
    # -------------------------------------------------------
    @staticmethod
    def register_all_admins(app_label=None):
        all_models = apps.get_models()
        for model in all_models:
            if issubclass(model, AutoAdminModel) and model is not AutoAdminModel:
                if app_label is None or model._meta.app_label == app_label:
                    model.register_admin()