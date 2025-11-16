from drofji_automatically_django_admin import fields, models


class Product(models.AutoAdminModel):
    name = fields.AutoAdminCharField(max_length=200)
    price = fields.AutoAdminDecimalField(max_digits=10, decimal_places=2)
    available = fields.AutoAdminBooleanField(default=True)


class Customer(models.AutoAdminModel):
    first_name = fields.AutoAdminCharField(max_length=100)
    last_name = fields.AutoAdminCharField(max_length=100)
    email = fields.AutoAdminEmailField(show_in_list=False, max_length=200)
    active = fields.AutoAdminBooleanField(default=True)
