from django.db import models

# Create your models here.


class Note(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    content = models.TextField()


class TodoList(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)


class Todo(models.Model):
    task = models.CharField(max_length=200)
    Parent = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

