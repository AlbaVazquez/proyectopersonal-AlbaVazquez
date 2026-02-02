from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class TechniqueChoices(models.TextChoices):
    DIGITAL = 'DIG', 'Digital'
    VECTOR = 'VEC', 'Vector'
    PIXEL_ART = 'PIX', 'Pixel Art'
    WATERCOLOR = 'ACU', 'Watercolor'
    TEMPERA = 'TEM', 'Tempera'
    OIL = 'OLE', 'Oil'
    ACRYLIC = 'ACR', 'Acrylic'
    GOUACHE = 'GOU', 'Gouache'
    GRAPHITE = 'GRF', 'Graphite'
    INK = 'TIN', 'Ink'
    CHARCOAL = 'CAR', 'Charcoal'
    PASTEL = 'PAS', 'Pastel'
    MARKER = 'MAR', 'Marker'
    MIXED_MEDIA = 'MIX', 'Mixed Media'
    COLLAGE = 'COL', 'Collage'
    SKETCH = 'BOC', 'Sketch'
    OTHER = 'OTR', 'Other'
    

class User(AbstractUser):
    pass

class Challenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    
class Artwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    final_image = models.ImageField(upload_to='artworks/final/')
    description = models.TextField(blank=True, null=True)
    technique = models.CharField(max_length=3, choices=TechniqueChoices.choices, default=TechniqueChoices.SKETCH)
    video_timelapse = models.FileField(upload_to='artworks/timelapses/', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('Start date cannot be after end date.')
    
class ProgressPhoto(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='artworks/progress/')
    order = models.IntegerField(default=1)
    
class PrivateComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)