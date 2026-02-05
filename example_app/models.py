from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db import models as django_models
from drofji_automatically_django_admin import fields as drofji_fields, models as drofji_models
from drofji_automatically_django_admin import validators


class Product(drofji_models.AutoAdminModel):
    name = drofji_fields.AutoAdminCharField(
        max_length=200,
        verbose_name=_("Name")
    )
    full_info2 = drofji_fields.AutoAdminFunctionField(
        func=lambda obj: f"{obj.name} — {obj.price}$",
        verbose_name=_("Full Info1"),
        show_in_list=True
    )
    price = drofji_fields.AutoAdminDecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price")
    )
    available = drofji_fields.AutoAdminBooleanField(
        default=True, verbose_name=_("Available")
    )
    full_info1 = drofji_fields.AutoAdminFunctionField(
        func=lambda obj: f"{obj.name} — {obj.price}$",
        verbose_name=_("Full Info"),
        show_in_list=True
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class Customer(drofji_models.AutoAdminModel):

    first_name = drofji_fields.AutoAdminCharField(
        max_length=100,
        verbose_name=_("First Name")
    )
    last_name = drofji_fields.AutoAdminCharField(
        max_length=100,
        verbose_name=_("Last Name")
    )
    origin = drofji_fields.AutoAdminCharField(
        max_length=100,
        verbose_name=_("Origin"),
        choices=[
            ('status_a', 'Status A'),
            ('status_b', 'Status B'),
            ('status_c', 'Status C')
        ],
        show_in_list=False,
        filterable=True
    )
    origin_display = drofji_fields.AutoAdminStatusBadgeField(
        field_name='origin',
        verbose_name=_("Origin 1"),
        choices=[
            drofji_fields.AutoAdminStatusBadgeFieldChoice(
                'status_a',
                text_html_color='#721C24',
                background_html_color='#F8D7DA',
                border_html_color='#F5C6CB'
            ),
            drofji_fields.AutoAdminStatusBadgeFieldChoice(
                'status_b',
                text_html_color='#856404',
                background_html_color='#FFF3CD',
                border_html_color='#FFEEBA'
            ),
            drofji_fields.AutoAdminStatusBadgeFieldChoice(
                'status_c',
                text_html_color='#155724',
                background_html_color='#D4EDDA',
                border_html_color='#C3E6CB'
            ),
        ],
        style_arguments={}
    )
    email = drofji_fields.AutoAdminEmailField(
        show_in_list=False,
        max_length=200,
        verbose_name=_("Email")
    )
    active = drofji_fields.AutoAdminBooleanField(
        default=True,
        verbose_name=_("Is Active")
    )

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
    total = drofji_fields.AutoAdminDecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Total"),
        filterable=True
    )
    config = drofji_fields.AutoAdminFileField(
        verbose_name=_("Configuration"),
        upload_to="configs/",
        allowed_extensions=[validators.FileExtensionEnum.JSON],
        allowed_encodings=[validators.FileEncodingEnum.UTF8],
        max_size_bytes=512 * 1024  # 512 KB
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
