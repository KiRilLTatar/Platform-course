from django.db import models
from users.models import User

# Create your models here.
class Couse(models.Model):
    title = models.CharField(max_length=256)
    promo = models.FileField(upload_to='courses/materials/', blank=True, null=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    update_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
    

class Module(models.Model):
    course = models.ForeignKey(Couse, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=256)
    description = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()

    class Meta: 
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} – {self.title}"
    

class Material(models.Model):
    MATERIAL_TYPE = (
        ('video', 'Видео'),
        ('text', 'Текст'),
        ('image', 'Изображение'),
    )

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='materials', null=True, blank=True)
    title = models.CharField(max_length=256)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='courses/materials/', blank=True, null=True)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPE)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        if self.lesson and self.lesson.module:
            return f"{self.lesson.module.title} → {self.lesson.title} → {self.title}"
        elif self.lesson:
            return f"{self.lesson.title} → {self.title}"
        return self.title