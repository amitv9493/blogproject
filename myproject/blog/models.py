# from django.contrib.auth.models import User
# from django.db import models
# from django.utils import timezone
# # Create your models here.

# class Post(models.Model):
#     # MAKING CHOICES WITH THIS Class
#     class Status(models.TextChoices):
#         DRAFT = 'DF', 'Draft'
#         PUBLISHED = 'PB', 'Published'

#     title = models.CharField(max_length=250)
#     slug = models.SlugField(max_length=250)
#     author = models.ForeignKey(User, on_delete= models.CASCADE, related_name='blog_posts')

#     body = models.TextField()
#     publish = models.DateTimeField(default=timezone.now)
#     created = models.DateTimeField(auto_now_add= True)
#     updated = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=2,
#                               choices=Status.choices,
#                               default=Status.DRAFT)

#     class meta:
#         ordering = ['-publish']
#         indexes = [models.Index(fields=['-publish'])]

#     def __str__(self):
#         return self.title


# USE THIS COMMAND IF THE MIGRATIONS DID NOT WORK PROPERLY
'''python manage.py migrate --run-syncdb '''

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse

"Creating custom Manager"


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug,
        ])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField( max_length=50)
    email = models.EmailField( max_length=254)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.body}"