import typing
from random import choice

from django.db import models
from django.utils.html import format_html
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

        autocomplete = kwargs.get('autocomplete')

        if autocomplete is None:
            self.autocomplete = True if kwargs.get('choices') else False
        else:
            self.autocomplete = autocomplete


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

        auto_now = kwargs.get('auto_now', False)
        auto_now_add = kwargs.get('auto_now_add', False)

        if not (auto_now or auto_now_add):
            kwargs['editable'] = editable

        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable


class AutoAdminTimeField(models.TimeField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=False,
                 filterable=True,
                 editable=True,
                 **kwargs):

        auto_now = kwargs.get('auto_now', False)
        auto_now_add = kwargs.get('auto_now_add', False)

        if not (auto_now or auto_now_add):
            kwargs['editable'] = editable

        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable


class AutoAdminDateTimeField(models.DateTimeField, AutoAdminField):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=False,
                 filterable=True,
                 editable=True,
                 **kwargs):

        auto_now = kwargs.get('auto_now', False)
        auto_now_add = kwargs.get('auto_now_add', False)

        if not (auto_now or auto_now_add):
            kwargs['editable'] = editable

        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable


class AutoAdminForeignKey(models.ForeignKey):
    def __init__(self, *args,
                 show_in_list=True,
                 searchable=True,
                 filterable=True,
                 editable=True,
                 autocomplete=True,
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


class AutoAdminStatusBadgeFieldChoice:
    def __init__(
            self, status_string: str,
            text_html_color="#333333",
            background_html_color="#F5F5F5",
            border_html_color="#A9A9A9"):
        self.status_string = status_string
        self.text_html_color = text_html_color
        self.background_html_color = background_html_color
        self.border_html_color = border_html_color

    def get_html_choice(self, field_display, style_arguments: dict):

        styles = {
            'color': self.text_html_color,
            'padding': '3px',
            'padding-left': '10px',
            'padding-right': '10px',
            'white-space': 'nowrap',
            'border-radius': '25px',
            'background-color': self.background_html_color,
            'border': f'2px solid {self.border_html_color}',
        }
        styles.update(style_arguments)
        style_string = "; ".join([f"{k}: {v}" for k, v in styles.items()])

        formated_html = format_html(
            '<a style="{}">{}</a>',
            style_string,
            field_display
        )
        return formated_html


class AutoAdminStatusBadgeField(AutoAdminFunctionField):
    def __init__(self, *args,
                 field_name=None,
                 choices: typing.List[AutoAdminStatusBadgeFieldChoice],
                 verbose_name=None,
                 style_arguments: dict = None,
                 **kwargs):

        self.choices = choices
        self.field_name = field_name
        self.style_arguments = style_arguments or {}

        super().__init__(
            func=self.get_html_choice,
            verbose_name=verbose_name,
            safe_html=True,
            *args, **kwargs
        )

    def get_html_choice(self, obj):

        field_value = getattr(obj, self.field_name, "")
        display_method_name = f"get_{self.field_name}_display"
        display_method = getattr(obj, display_method_name, None)
        field_display = display_method() if display_method else field_value

        for choice in self.choices:
            if choice.status_string == field_value:
                return choice.get_html_choice(field_display, self.style_arguments)

        return field_display
