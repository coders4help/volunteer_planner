from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify


class Notification(models.Model):
    creation_date = models.DateField(auto_now=True)
    title = models.CharField(max_length=255, verbose_name="Titel")
    subtitle = models.CharField(max_length=255, verbose_name="Untertitel", null=True, blank=True)
    text = models.TextField(max_length=20055, verbose_name="Artikeltext")
    slug = models.SlugField(auto_created=True, max_length=255)
    location = models.ForeignKey('scheduler.Location')

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(Notification, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title