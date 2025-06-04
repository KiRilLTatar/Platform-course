from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=256)
    description = models.TextField(default="")
    is_cheater = models.BooleanField(default=False)
    data_joined = models.DateField(auto_now_add=True)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
  
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.IntegerField()
    comleted_modules = models.JSONField(default=list)
    last_accessed = models.DateField(auto_now=True)
    completion_percent = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "Progress records"
        unique_together = ("user", "course_id")

    def __str__(self):
        return f"{self.user.username} - Course {self.course_id}"
    
    def update_progress(self, module_id, total_modules):
        if module_id not in self.comleted_modules:
            self.comleted_modules.append(module_id)
            self.completion_percent = round((len(self.comleted_modules) / total_modules) * 100, 2)
            self.last_accessed = timezone.now()
            self.save()
