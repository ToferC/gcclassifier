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
    language = models.CharField(max_length=8, choices=LANGUAGES,
    	default='EN')
    published = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag', blank=True)
    communities = models.ManyToManyField('Community', blank=True)
    slug = models.SlugField(unique=True, max_length=255)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Document, self).save(*args, **kwargs)


class Community(models.Model):
    name = models.CharField(max_length=128)
    creator = models.ForeignKey(User)
    user_generated = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/community_images/%Y/%m/%d/%H_%M_%S',
        null=True, blank=True, default='images/community_images/nothing.jpg')

    slug = models.SlugField(unique=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Community, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=128)
    creator = models.ForeignKey(User)
    user_generated = models.BooleanField(default=False)
    community = models.ManyToManyField(Community)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/tag_images/%Y/%m/%d/%H_%M_%S',
        null=True, blank=True, default='images/tag_images/nothing.jpg')

    slug = models.SlugField(unique=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)