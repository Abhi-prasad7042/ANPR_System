from django.db import models

# Create your models here.
class ImageOCR(models.Model):
    image = models.ImageField(upload_to="numbers")

    def __str__(self) -> str:
        return f"{self.image}"