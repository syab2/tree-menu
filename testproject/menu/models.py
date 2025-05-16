from django.db import models # type: ignore
from django.urls import reverse # type: ignore
from django.utils.text import slugify

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Menu Name')
    slug = models.SlugField(max_length=50, null=True, unique=True, verbose_name='Menu Slug')

    class Meta:
        verbose_name = 'menu'
        verbose_name_plural = 'menus'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    named_url = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = 'menu item'
        verbose_name_plural = 'menu items'


    def __str__(self):
        return self.title

    def get_url(self):
        if self.named_url:
            return self.named_url
        return self.url
