from django.contrib import admin

from apps.inventory.models import Inventory


class InventoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Inventory._meta.fields]
    history_list_display = ["status"]


admin.site.register(Inventory, InventoryAdmin)
