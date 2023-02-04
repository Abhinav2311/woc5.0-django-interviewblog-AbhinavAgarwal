import re
from django.db import models
from ckeditor.fields import RichTextField  
####
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.timezone import now


# Create your models here.
class Post(models.Model):

    OFFER_CHOICES = [
        ('Select Offer Type', (
        ('Summer Internship','Summer Internship'),
        ('Winter Internship Only','Winter Internship Only'),
        ('Job Only','Job Only'),
        ('Winter Internship and Job','Winter Internship and Job'),
            )
        ),   
    ]

    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,unique=True,blank=False)
    slug = models.SlugField(max_length=100,editable=False, null=True, blank=True)
    # slug = AutoSlugField(null=True,blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.CharField(max_length=30,blank=False)
    year = models.IntegerField(blank=False)
    offer_type = models.CharField(max_length=30, choices=OFFER_CHOICES, default='Select Offer Type',blank=False)
    job_profile = models.CharField(max_length=30,blank=False)
    content = RichTextField(blank=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bookmarks = models.ManyToManyField(User, related_name='bookmark', default=None, blank=True)

    def get_absolute_url(self):
        return reverse('blog_detail',args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.title)
            unique_slugify(self, self.slug)
            
        return super().save(*args, **kwargs)

#For generating Unique slug
def unique_slugify(instance, value, slug_field_name='slug', queryset=None, slug_separator='-'):
    
        slug_field = instance._meta.get_field(slug_field_name)

        slug = getattr(instance, slug_field.attname)
        slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
        slug = slugify(value)
        if slug_len:
            slug = slug[:slug_len]
        slug = _slug_strip(slug, slug_separator)
        original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
        if queryset is None:
            queryset = instance.__class__._default_manager.all()
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
        next = 2
        while not slug or queryset.filter(**{slug_field_name: slug}):
            slug = original_slug
            end = '%s%s' % (slug_separator, next)
            if slug_len and len(slug) + len(end) > slug_len:
                slug = slug[:slug_len-len(end)]
                slug = _slug_strip(slug, slug_separator)
            slug = '%s%s' % (slug, end)
            next += 1

        setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    degree = models.CharField(max_length=30,blank=True, null=True)
    program = models.CharField(max_length=70,blank=True, null=True)
    graduation = models.IntegerField(blank=True, null=True)
    profile_pic = models.ImageField(default="logo_user2.png",null=True, blank=True)

    def __str__(self):
        return str(self.user) 

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + " by " + self.user.username
    


