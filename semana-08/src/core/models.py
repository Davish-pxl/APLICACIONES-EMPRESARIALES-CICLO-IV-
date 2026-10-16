from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ['-created_at']