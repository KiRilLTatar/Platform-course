from django.contrib import admin
from courses.models import Couse, Module, Lesson, Material


# Register your models here.
@admin.register(Couse)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "description", "author__username")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order")
    list_filter = ("module__course",)
    search_fields = ("title",)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "get_lesson", "get_module", "material_type")

    def get_lesson(self, obj):
        try:
            return obj.lesson.title
        except AttributeError:
            return "—"
    get_lesson.short_description = "Lesson"

    def get_module(self, obj):
        try:
            return obj.lesson.module.title
        except AttributeError:
            return "—"
    get_module.short_description = "Module"
