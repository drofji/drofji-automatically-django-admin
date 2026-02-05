# drofji_automatically_django_admin/models.py
from PIL.ImageCms import applyTransform
from django.db import models
from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.apps import apps
from django.db.models import DateField
from django.utils.safestring import mark_safe
from drofji_automatically_django_admin import fields as drofji_fields
from drofji_automatically_django_admin.fields import (
                            AutoAdminDateField, AutoAdminDateTimeField,
                            AutoAdminIntegerField, AutoAdminFloatField, AutoAdminDecimalField
                        )
from rangefilter.filters import DateRangeFilter, NumericRangeFilter


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
        meta_fields = {f.name: f for f in cls._meta.get_fields() if
                       hasattr(f, "name") and not (f.one_to_many or f.one_to_one or f.many_to_many)}
        meta_fields_related = {f.name: f for f in cls._meta.get_fields() if
                       hasattr(f, "name") and (f.many_to_one or f.many_to_many)}
        attr_fields = cls.__dict__

        #####################
        #   SHOW IN FORM    #
        #####################

        form_fields = [fn for fn, fo in meta_fields.items() if getattr(fo, "show_in_form", True)]

        #####################
        #   SHOW IN LIST    #
        #####################

        list_display = [fn for fn, fo in meta_fields.items() if getattr(fo, "show_in_list", True)]

        ###################
        #   SEARCHABLE    #
        ###################

        search_fields = [fn for fn, fo in meta_fields.items() if getattr(fo, "searchable", False)]

        ###################
        #   FILTERABLE    #
        ###################

        list_filter = []
        for meta_field_name, meta_field in meta_fields.items():

            if not getattr(meta_field, "filterable", False):
                continue

            if isinstance(meta_field, (models.DateField, models.DateTimeField, models.TimeField)):
                list_filter.append((meta_field_name, DateRangeFilter))

            elif isinstance(meta_field, (models.IntegerField, models.FloatField, models.DecimalField)):
                list_filter.append((meta_field_name, NumericRangeFilter))

            elif isinstance(meta_field, models.ForeignKey):

                filter_class_name = f"{meta_field_name.capitalize()}Filter"
                DynamicFilter = type(filter_class_name, (AutocompleteFilter,), {
                    'title': meta_field.verbose_name or meta_field_name,
                    'field_name': meta_field_name,
                })
                if DynamicFilter not in list_filter:
                    list_filter.append(DynamicFilter)
            else:
                list_filter.append(meta_field_name)

        #####################
        #   AUTOCOMPLETE    #
        #####################

        autocomplete_fields = [fn for fn, fo in meta_fields_related.items() if getattr(fo, "autocomplete", True)]

        ########################
        #   FUNCTION FIELDS    #
        ########################

        for attr_field_name, attr_field in list(attr_fields.items()):

            if isinstance(attr_field, drofji_fields.AutoAdminFunctionField):
                method_name = f"autoAdminFunctionField{str(attr_field_name).capitalize()}"

                def make_func(f):
                    @admin.display(description=getattr(f, 'verbose_name', '') or getattr(f, 'name', ''))
                    def _func(self, obj):
                        value_to_display = f.get_display_value(obj)
                        return value_to_display

                    return _func

                if not hasattr(cls, 'admin_overrides'):
                    cls.admin_overrides = {}
                cls.admin_overrides[method_name] = make_func(attr_field)
                list_display.append(method_name)

        if 'id' in list_display:
            list_display.remove('id')
            list_display.insert(0, 'id')

        return form_fields, list_display, search_fields, list_filter, autocomplete_fields

    # ---------------------------------------------------
    # Register model in Django admin
    # ---------------------------------------------------
    @classmethod
    def register_admin(cls):
        if not cls.admin_enabled:
            return

        # Get fields
        fields, list_display, search_fields, list_filter, autocomplete_fields = cls.get_admin_fields()

        class Media:
            css = {"all": getattr(cls, "admin_css", [])}
            js = getattr(cls, "admin_js", [])

        result_js_files = {
            "admin/js/vendor/jquery/jquery.js",
            "admin/js/jquery.init.js",
            "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js",
            "drofji_automatically_django_admin/admin.js"
        }
        result_css_files = {
            "drofji_automatically_django_admin/admin.css",
            "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css",
        }

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
