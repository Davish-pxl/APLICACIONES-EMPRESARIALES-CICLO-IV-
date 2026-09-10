from django.contrib import admin
from .models import Item

# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Item en el panel de administración
    """
    # Camos que se muestran en la lista
    list_display = ('id', 'name', 'description_short', 'created_at', 'days_ago')
    
    list_display_links = ('id', 'name')
    
    list_filter = ('created_at',)
    
    search_fields = ('name', 'description')
    
    ordering = ('-created_at',)
    
    readonly_fields = ('created_at',)
    
    list_per_page = 20
    
    def description_short(self, obj):
        """Muestra los primeros 50 caracteres de la descripción"""
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return 'Sin descripción'
    description_short.short_description = 'Descripción'
    
    def days_ago(self, obj):
        """Muestra cuántos días pasaron desde la creación"""
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        days = delta.days
        if days == 0:
            return 'Hoy'
        elif days == 1:
            return 'Ayer'
        else:
            return f'{days} días'
    days_ago.short_description = 'Antigüedad'
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('name', 'description')
        }),
        ('Información del Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)  # Colapsable
        }),
    )