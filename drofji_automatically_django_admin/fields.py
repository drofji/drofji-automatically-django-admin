import typing

from django.db import models
from django.utils.safestring import mark_safe
from drofji_automatically_django_admin import validators
from django import forms


# ===========================================================
# Custom AutoAdmin Fields
# ===========================================================


class AutoAdminField:
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=True,
                 filterable=False,
                 editable=True,
                 **kwargs):

        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable

        super().__init__(*args, **kwargs)


class AutoAdminNotDatabaseField:
    pass


# -----------------------------
# Define AutoAdmin field types
# -----------------------------
class AutoAdminCharField(models.CharField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=True,
                 filterable=False,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminTextField(models.TextField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=False,
                 filterable=False,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminFileField(models.FileField, AutoAdminField):
    def __init__(
            self,
            show_in_list=False,
            searchable=False,
            filterable=False,
            editable=True,
            allowed_extensions: typing.List[typing.Union[validators.FileExtensionEnum, str]] = None,
            allowed_encodings: typing.List[typing.Union[validators.FileEncodingEnum, str]] = None,
            max_size_bytes: int = None,
            *args, **kwargs
    ):
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable

        self.allowed_extensions = allowed_extensions
        self.max_size_bytes = max_size_bytes

        self.file_validator = validators.FileValidator(
            allowed_extensions=allowed_extensions,
            allowed_encodings=allowed_encodings,
            max_size_bytes=max_size_bytes
        )

        kwargs.setdefault('validators', []).append(self.file_validator)

        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        if self.allowed_extensions:
            accept_value = ",".join([
                f".{ext.value if hasattr(ext, 'value') else ext}"
                for ext in self.allowed_extensions
            ])
            kwargs.update({
                "widget": forms.FileInput(attrs={'accept': accept_value})
            })
        return super().formfield(**kwargs)


class AutoAdminFilePathField(models.FilePathField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=False,
                 searchable=False,
                 filterable=False,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminJSONField(models.JSONField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=False,
                 searchable=False,
                 filterable=False,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminIntegerField(models.IntegerField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=False,
                 filterable=True,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminFloatField(models.FloatField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=False,
                 filterable=False,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminDecimalField(models.DecimalField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=False,
                 filterable=False,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminBooleanField(models.BooleanField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=False,
                 filterable=True,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminDateField(models.DateField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=False,
                 filterable=True,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminTimeField(models.TimeField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=False,
                 filterable=True,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminDateTimeField(models.DateTimeField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=False,
                 filterable=True,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminForeignKey(models.ForeignKey):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=True,
                 filterable=True,
                 editable=True,
                 autocomplete=False,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable
        self.autocomplete = autocomplete


class AutoAdminEmailField(models.EmailField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=True,
                 filterable=False,
                 editable=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminFunctionField(AutoAdminNotDatabaseField):
    def __init__(self, func, verbose_name=None, show_in_list=True,
                 show_in_form=True, safe_html=False, *args, **kwargs):
        if not callable(func):
            raise ValueError("AutoAdminFunctionField requires a callable 'func'.")

        self.func = func
        self.verbose_name = verbose_name
        self.show_in_list = show_in_list
        self.show_in_form = show_in_form
        self.safe_html = safe_html

        super().__init__()

    def get_display_value(self, obj):
        value = self.func(obj)
        if self.safe_html:
            from django.utils.safestring import mark_safe
            return mark_safe(value)
        return value
