from django.db import models
from django.conf import settings


# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=50)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='admin_group_set')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users_group_set')


class Image(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, default=None)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='owner_image_set',
                              null=True, blank=True, default=0)
    custom_name = models.CharField(max_length=50, blank=True, null=True, default=None)
    upload_ip_address = models.GenericIPAddressField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users_image_set', blank=True)
    groups = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='groups_image_set', blank=True)
    added = models.DateTimeField(auto_now_add=True)
    lease = models.DateTimeField()
    model_pic = models.ImageField()

class Tag(models.Model):
    name = models.CharField(max_length=50)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

