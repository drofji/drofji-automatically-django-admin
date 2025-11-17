from django.db import models

# ===========================================================
# Custom AutoAdmin Fields
# ===========================================================


# -----------------------------
# Define AutoAdmin field types
# -----------------------------
class AutoAdminCharField(models.CharField):
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


class AutoAdminTextField(models.TextField):
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


class AutoAdminFileField(models.FileField):
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


class AutoAdminFilePathField(models.FilePathField):
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


class AutoAdminJSONField(models.JSONField):
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


class AutoAdminIntegerField(models.IntegerField):
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


class AutoAdminFloatField(models.FloatField):
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


class AutoAdminDecimalField(models.DecimalField):
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


class AutoAdminBooleanField(models.BooleanField):
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


class AutoAdminDateField(models.DateField):
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

class AutoAdminTimeField(models.TimeField):
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

class AutoAdminDateTimeField(models.DateTimeField):
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
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.show_in_list = show_in_list
        self.searchable = searchable
        self.filterable = filterable
        self.editable = editable


class AutoAdminEmailField(models.EmailField):
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
