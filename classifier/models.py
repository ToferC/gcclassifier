from django.db import models
from django.utils import timezone
from django.db.models import F
from django.template.defaultfilters import slugify

# Create your models here.

class Document(models.Model):

	title = models.CharField(max_length=128)
    creator = models.ForeignKey(User)
    created_date = models.DateField(auto_now=True)
    content = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag', blank=True)
    communities = models.ManyToManyField('Community', blank=True)
    slug = models.SlugField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Document, self).save(*args, **kwargs)


