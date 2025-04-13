from better_filter_widget import BetterFilterWidget
from django.contrib import admin, messages
from django_no_queryset_admin_actions import NoQuerySetAdminActionsMixin

from ..common.admin import AutoFilterHorizontalMixin
from ..common.sticker_printer import batch_print_qr
from ..common.utils import check_expiration_date, get_expiration_days
from .models import Category, DemandTag, Product, Supply
from .qr import bulk_generate_qrs_for_supplies


class CategoryAdmin(admin.ModelAdmin):
    pass


class DemandTagAdmin(AutoFilterHorizontalMixin, admin.ModelAdmin):
    pass


class ProductAdmin(AutoFilterHorizontalMixin, admin.ModelAdmin):
    list_display = ["__str__", "bar_code", "volume", "get_categories"]

    def get_categories(self, obj: Product):
        return " | ".join([cat.name for cat in obj.categories.all()])

    get_categories.short_description = "Categories"


class SupplyAdmin(NoQuerySetAdminActionsMixin, admin.ModelAdmin):
    list_display = [
        "__str__",
        "amount",
        "expiration_date",
        "get_expiration_days",
        "get_expired",
        "scheduled_print",
        "printed_once",
    ]

    readonly_fields = ["created_at", "updated_at"]

    def get_expired(self, obj: Supply) -> str:
        x_ascii = "\u274c"
        return f"{x_ascii}" if check_expiration_date(obj) else ""

    get_expired.short_description = "Expired"

    def get_expiration_days(self, obj: Supply) -> int:
        return get_expiration_days(obj)

    get_expiration_days.short_description = "Days left"

    @admin.action(description="Schedule for print")
    def schedule_for_print(self, request, queryset):
        queryset.schedule_for_print()

    @admin.action(description="Schedule all not-printed for print")
    def schedule_not_printed_for_print(self, request):
        qs = Supply.objects.not_printed()
        qs.schedule_for_print()

    @admin.action(description="Unschedule all")
    def unschedule_all(self, request):
        Supply.objects.un_schedule_for_print()

    @admin.action(description="Print selected instantly")
    def instant_print(self, request, queryset):
        queryset.prefetch_product()
        self._perform_print(queryset, request)

    @admin.action(description="Print qr-codes batch")
    def batch_print(self, request):
        qs = Supply.objects.scheduled_for_print()
        self._perform_print(qs, request)

    @staticmethod
    def _perform_print(qs, request):
        try:
            images_list = bulk_generate_qrs_for_supplies(qs)
            result = batch_print_qr(images_list)
            qs.mark_as_printed()

            if result:
                messages.add_message(request, messages.INFO, "Printed successfully!")
            else:
                messages.add_message(request, messages.WARNING, "Nothing to print!")
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Printing error! '{e}'")

    actions = [
        "schedule_not_printed_for_print",
        "schedule_for_print",
        "batch_print",
        "instant_print",
        "unschedule_all",
    ]
    no_queryset_actions = [
        "batch_print",
        "schedule_not_printed_for_print",
        "unschedule_all",
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(DemandTag, DemandTagAdmin)
