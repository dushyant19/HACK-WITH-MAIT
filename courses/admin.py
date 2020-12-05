from django.contrib import admin
from .models import Subject, Course, Module, Content, Text, File, Image, Video, Announcement, Discussion
from django.contrib import admin

# use memcache admin index site
admin.site.index_template = 'memcache_status/admin_index.html'

admin.site.register(Content)
admin.site.register(Text)
admin.site.register(File)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Announcement)
admin.site.register(Discussion)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created', 'student_courses']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
