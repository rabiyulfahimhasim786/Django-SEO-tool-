from django.db import models

class textarticle(models.Model):
    url = models.URLField(max_length=255)


class Keyword(models.Model):
    Keywords = models.CharField(max_length=255, blank=False)
    #Keywords = models.URLField(max_length=255, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Genre(models.Model):
    name = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.TextField(blank=False)
    year = models.TextField(blank=False)
    filmurl = models.TextField(blank=False)
    # genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    genre = models.TextField(blank=False)
    
    def __str__(self):
        return self.title
    
