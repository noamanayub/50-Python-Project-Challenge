from django.db import models
from django.urls import reverse

class Professor(models.Model):
    profile_picture = models.ImageField(upload_to='professors/', blank=True, null=True)
    name = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    research_interests = models.TextField()
    email = models.EmailField()
    h_index = models.IntegerField()
    famous_articles = models.TextField()
    google_scholar_url = models.URLField()
    researchgate_url = models.URLField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('professor_detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['name']
