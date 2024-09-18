from django.db import models


class Note (models.Model):
  title = models.CharField(max=100)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True) 
  updated_at = models.DateTimeField(auto_now=True)