# drofji_automatically_django_admin/models.py

from django.db import models
from django.contrib import admin
from django.apps import apps
from django.utils.safestring import mark_safe
from drofji_automatically_django_admin import fields as drofji_fields

# Optional range filters
try:
    from rangefilter.filters import DateRangeFilter, NumericRangeFilter

    RANGEFILTER_AVAILABLE = True
except ImportError:
    RANGEFILTER_AVAILABLE = False


# -------------------------------------------------------
# Custom ID formatter: faded leading zeros
# -------------------------------------------------------
@staticmethod
@admin.display(description="ID")
def formatted_id(obj):
    raw = f"{obj.id:06d}"
    i = 0
    while i < len(raw) and raw[i] == "0":
        i += 1
    leading = raw[:i]
    number = raw[i:] or "0"
    return mark_safe(f'<span class="faded-zeros">{leading}</span>{number}')


# -------------------------------------------------------
# Base AutoAdmin model
# -------------------------------------------------------
class AutoAdminModel(models.Model):
    admin_enabled = True
    js_admin_files = []
    css_admin_files = []
    admin_sections = []

    class Meta:
        abstract = True

    def __str__(self):
        # Display 'name' or 'alias' if available
        if hasattr(self, "name") and self.name:
            return str(self.name)
        if hasattr(self, "alias") and self.alias:
            return str(self.alias)
        return super().__str__()

    # ---------------------------------------------------
    # Compute admin fields dynamically
    # ---------------------------------------------------
    @classmethod
    def get_admin_fields(cls):
        meta_fields = {f.name: f for f in cls._meta.get_fields() if hasattr(f, "name")}

        list_display = []
        search_fields = []
        list_filter = []
        autocomplete_fields = []

        for attr_name in list(cls.__dict__.keys())[::-1]:
            attr = getattr(cls, attr_name)
            meta_field = meta_fields[attr_name] if attr_name in meta_fields.keys() else None

            if isinstance(attr, (models.query_utils.DeferredAttribute, drofji_fields.AutoAdminField)):

                if meta_field is not None and (not hasattr(meta_field,
                                                           'name') or meta_field.one_to_many or meta_field.one_to_one or meta_field.many_to_many):
                    continue

                if getattr(meta_field, "show_in_list", True):
                    list_display.append(attr_name)

                if getattr(meta_field, "searchable", False):
                    search_fields.append(attr_name)
                    print('add to search', attr_name)

                if getattr(meta_field, "filterable", False):
                    if RANGEFILTER_AVAILABLE:
                        from drofji_automatically_django_admin.fields import (
                            AutoAdminDateField, AutoAdminDateTimeField,
                            AutoAdminIntegerField, AutoAdminFloatField, AutoAdminDecimalField
                        )
                        if isinstance(meta_field, (AutoAdminDateField, AutoAdminDateTimeField)):
                            list_filter.append((attr_name, DateRangeFilter))
                        elif isinstance(meta_field,
                                        (AutoAdminIntegerField, AutoAdminFloatField, AutoAdminDecimalField)):
                            list_filter.append((attr_name, NumericRangeFilter))
                        else:
                            list_filter.append(attr_name)
                    else:
                        list_filter.append(attr_name)

                if isinstance(attr, drofji_fields.AutoAdminFunctionField):
                    method_name = f"{attr_name}"

                    def make_func(f):
                        @admin.display(description=getattr(f, 'verbose_name', '') or getattr(f, 'name', ''))
                        def _func(self, obj):
                            value_to_display = f.get_display_value(obj)
                            return value_to_display

                        return _func

                    cls.admin_overrides = getattr(cls, 'admin_overrides', {})
                    cls.admin_overrides[method_name] = make_func(attr)

                # FK/M2M autocomplete support
                autocomplete_fields = [
                    f.name for n, f in meta_fields.items()
                    if hasattr(f, "remote_field") and getattr(f, "autocomplete", False)
                ]

            if 'id' in list_display:
                list_display.remove('id')
                list_display.insert(0, 'id')

        return list_display, search_fields, list_filter, autocomplete_fields

    # ---------------------------------------------------
    # Register model in Django admin
    # ---------------------------------------------------
    @classmethod
    def register_admin(cls):
        if not cls.admin_enabled:
            return

        # Get fields
        list_display, search_fields, list_filter, autocomplete_fields = cls.get_admin_fields()

        class Media:
            css = {"all": getattr(cls, "admin_css", [])}
            js = getattr(cls, "admin_js", [])

        result_js_files = {"drofji_automatically_django_admin/admin.js"}
        result_css_files = {"drofji_automatically_django_admin/admin.css"}

        js_to_add = getattr(cls, 'js_admin_files', [])
        if isinstance(js_to_add, (list, tuple, set)):
            result_js_files.update(js_to_add)
        elif isinstance(js_to_add, str):
            result_js_files.add(js_to_add)

        css_to_add = getattr(cls, 'css_admin_files', [])
        if isinstance(css_to_add, (list, tuple, set)):
            result_css_files.update(css_to_add)
        elif isinstance(css_to_add, str):
            result_css_files.add(css_to_add)

        admin_attrs = {
            "search_fields": search_fields,
            "list_filter": list_filter,
            "autocomplete_fields": autocomplete_fields,
            "formatted_id": formatted_id,
            "Media": type("Media", (), {
                "css": {"all": result_css_files},
                "js": result_js_files
            }),
        }

        # ---------------------------------------------------
        # Add AutoAdminFunctionField methods
        # ---------------------------------------------------

        # Add function fields to list_display
        admin_attrs["list_display"] = list_display

        # Apply admin overrides if defined
        overrides = getattr(cls, "admin_overrides", {})
        for k, v in overrides.items():
            admin_attrs[k] = v

        # Create dynamic ModelAdmin class
        admin_class = type(f"{cls.__name__}Admin", (admin.ModelAdmin,), admin_attrs)

        # Register in admin
        try:
            admin.site.register(cls, admin_class)
        except admin.sites.AlreadyRegistered:
            pass

    # ---------------------------------------------------
    # Register all children models automatically
    # ---------------------------------------------------
    @staticmethod
    def register_all_admins(app_label=None):
        for model in apps.get_models():
            if issubclass(model, AutoAdminModel) and model is not AutoAdminModel:
                if app_label is None or model._meta.app_label == app_label:
                    model.register_admin()
