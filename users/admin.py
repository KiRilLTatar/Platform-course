from django.contrib import admin
from users.models import User, Progress

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "full_name", "date_joined")


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course_id', 'completion_percent', 'last_accessed', 'module_count')
    list_filter = ('last_accessed', 'user')
    search_fields = ('user__username', 'course_id')
    ordering = ('-last_accessed',)
    readonly_fields = ('last_accessed', 'completion_percent')

    def module_count(self, obj):
        return len(obj.comleted_modules)
    module_count.short_description = "Завершено модулей"