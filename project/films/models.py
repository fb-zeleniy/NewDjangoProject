from django.db import models

class Film(models.Model):
    slug=models.SlugField(unique=True,blank=False,null=False)
    name=models.CharField(max_length=100,null=False,blank=False)
    author=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    year=models.DateField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




