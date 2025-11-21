from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db import models as django_models
from drofji_automatically_django_admin import fields as drofji_fields, models as drofji_models


class Product(drofji_models.AutoAdminModel):
    name = drofji_fields.AutoAdminCharField(max_length=200, verbose_name=_("Name"))
    price = drofji_fields.AutoAdminDecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    available = drofji_fields.AutoAdminBooleanField(default=True, verbose_name=_("Available"))

    @admin.display(description=_("Name (Bold)"))
    def bold_name(self, obj):
        return format_html("<b>{}</b>", obj.name)

    admin_overrides = {
        "bold_name": bold_name,
        "list_display": ["formatted_id", "bold_name", "price", "available"]
    }

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class Customer(drofji_models.AutoAdminModel):
    first_name = drofji_fields.AutoAdminCharField(max_length=100, verbose_name=_("First Name"))
    last_name = drofji_fields.AutoAdminCharField(max_length=100, verbose_name=_("Last Name"))
    email = drofji_fields.AutoAdminEmailField(show_in_list=False, max_length=200, verbose_name=_("Email"))
    active = drofji_fields.AutoAdminBooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")


class Order(drofji_models.AutoAdminModel):
    customer = drofji_fields.AutoAdminForeignKey(
        to=Customer,
        on_delete=django_models.PROTECT,
        verbose_name=_("Customer"),
        autocomplete=True,
    )
    total = drofji_fields.AutoAdminDecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total"))

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
