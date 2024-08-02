from django.contrib import admin

from apps.human_resources.models import Employee


# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Employee._meta.fields]
    history_list_display = ["status"]


admin.site.register(Employee, EmployeeAdmin)
