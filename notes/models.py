from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    content = models.TextField()


class TodoList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)


class Todo(models.Model):
    task = models.CharField(max_length=200)
    Parent = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

