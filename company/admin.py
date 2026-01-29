from django.contrib import admin

from company.models import Employee, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'parent',
        'level',
        'created_at',
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'surname',
        'first_name',
        'position',
        'salary',
        'hiring_date',
    )
