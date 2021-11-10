from django.contrib import admin
from .models import DepartmentModel, PositionModel, EmployeeModel


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class PositionAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "surname",
        "name",
        "department",
        "position",
        "hiring_date",
        "experience",
        "phone",
    ]


admin.site.register(DepartmentModel, DepartmentAdmin)
admin.site.register(PositionModel, PositionAdmin)
admin.site.register(EmployeeModel, EmployeeAdmin)
