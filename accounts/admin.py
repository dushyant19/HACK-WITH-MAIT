from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('role','is_approved')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Roles', {'fields': ('role',)}),
    )

admin.site.register(User,CustomUserAdmin)
admin.site.register(Student)
admin.site.register(StudentToCourses)
admin.site.register(Parent)
admin.site.register(Teacher)
# Register your models here.
