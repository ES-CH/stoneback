from django.contrib import admin

from apps.accounting.models import Accounting


class AccountingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Accounting._meta.fields]
    history_list_display = ["status"]


admin.site.register(Accounting, AccountingAdmin)
