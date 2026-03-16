from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name