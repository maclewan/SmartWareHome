from django.contrib import admin

from ..common.admin import AutoFilterHorizontalMixin
from ..common.utils import check_expiration_date, get_expiration_days
from .models import Category, DemandTag, Product, Supply


class CategoryAdmin(admin.ModelAdmin):
    pass


class DemandTagAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(AutoFilterHorizontalMixin, admin.ModelAdmin):
    list_display = ["__str__", "bar_code", "volume", "get_categories"]

    def get_categories(self, obj: Product):
        return " | ".join([cat.name for cat in obj.categories.all()])

    get_categories.short_description = "Categories"


class SupplyAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "amount",
        "expiration_date",
        "get_expiration_days",
        "get_expired",
    ]

    readonly_fields = ["created_at", "updated_at"]

    def get_expired(self, obj: Supply) -> str:
        x_ascii = "\u274c"
        return f"{x_ascii}" if check_expiration_date(obj) else ""

    get_expired.short_description = "Expired"

    def get_expiration_days(self, obj: Supply) -> int:
        return get_expiration_days(obj)

    get_expiration_days.short_description = "Days left"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(DemandTag, DemandTagAdmin)
