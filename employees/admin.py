from django.contrib import admin
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'position', 'salary', 'join_date')
    search_fields = ('name', 'email', 'position')
    list_filter = ('position', 'join_date')
    

admin.site.register(Employee, EmployeeAdmin)