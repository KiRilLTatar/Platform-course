from django.db import models
from courses.models import Module
from users.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone



# Create your models here.
class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    module = models.ForeignKey('courses.Module', on_delete=models.CASCADE, related_name='tests')
    is_published = models.BooleanField(default=False)
    passing_score = models.FloatField(default=70.0) 
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def clean(self):
        if not (0 <= self.passing_score <= 100):
            raise ValidationError("Проходной балл должен быть от 0 до 100")

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ('single', 'Single correct answer'),
        ('multiple', 'Multiple correct answers'),
        ('text', 'Text answer'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    order = models.PositiveIntegerField(default=0)  
    points = models.PositiveIntegerField(default=1)  
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.text[:50]}..." if len(self.text) > 50 else self.text


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_options')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0) 
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.text[:50]}..." if len(self.text) > 50 else self.text


class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)  
    is_passed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user} - {self.test} ({self.score}%)"
    
    def evaluate(self):
        total_earned = 0
        total_possible = 0

        for user_answer in self.user_answers.select_related('question').prefetch_related('answer_options'):
            question = user_answer.question
            total_possible += question.points

            is_correct = False

            if question.question_type == 'text':
                is_correct = user_answer.is_correct  
            elif question.question_type == 'single':
                correct_answers = question.answer_options.filter(is_correct=True).values_list('id', flat=True)
                selected = list(user_answer.answer_options.values_list('id', flat=True))
                is_correct = len(selected) == 1 and selected[0] in correct_answers
            elif question.question_type == 'multiple':
                correct_answers = set(question.answer_options.filter(is_correct=True).values_list('id', flat=True))
                selected = set(user_answer.answer_options.values_list('id', flat=True))
                is_correct = selected == correct_answers

            user_answer.is_correct = is_correct
            user_answer.points_earned = question.points if is_correct else 0
            user_answer.save()

            total_earned += user_answer.points_earned

        percent = round((total_earned / total_possible) * 100, 2) if total_possible > 0 else 0
        self.score = percent
        self.is_passed = percent >= self.test.passing_score
        self.completed_at = timezone.now()
        self.save()
        return self.score, self.is_passed


class UserAnswer(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_options = models.ManyToManyField(AnswerOption, blank=True) 
    text_answer = models.TextField(blank=True)  
    is_correct = models.BooleanField(default=False)
    points_earned = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.attempt.user} - {self.question.text[:30]}..."
    
    @property
    def answer_summary(self):
        if self.text_answer:
            return self.text_answer
        return ", ".join([opt.text for opt in self.answer_options.all()])
    
    def clean(self):
        if self.question.question_type == 'text':
            if not self.text_answer.strip():
                raise ValidationError("Для текстового вопроса необходимо ввести ответ.")
        else:
            if not self.answer_options.exists():
                raise ValidationError("Для выбора нужно указать хотя бы один ответ.")
