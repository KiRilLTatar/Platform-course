from django.contrib import admin
from tests.models import Test, Question, AnswerOption, TestAttempt, UserAnswer


# Register your models here.
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'is_published', 'passing_score', 'created_at')
    list_filter = ('is_published', 'module')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'test', 'question_type', 'order', 'points')
    list_filter = ('question_type', 'test')
    search_fields = ('text',)
    list_editable = ('order', 'points')
    ordering = ('test', 'order')

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Text'


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'question', 'is_correct', 'order')
    list_filter = ('is_correct', 'question__test')
    search_fields = ('text', 'question__text')
    list_editable = ('is_correct', 'order')
    ordering = ('question', 'order')

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Option'


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'started_at', 'completed_at', 'score', 'is_passed')
    list_filter = ('is_passed', 'test', 'user')
    search_fields = ('user__username', 'test__title')
    date_hierarchy = 'started_at'
    readonly_fields = ('started_at',)
    ordering = ('-started_at',)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'text_answer')
    search_fields = ('text_answer',)
