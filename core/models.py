# -*- coding: utf-8 -*-
import os
import hashlib
import socket
from django.db import models
from settings import UPLOAD_DIR

class Bundle(models.Model):

    def __unicode__(self):
        return u'Bundle %d' % self.id


def upload_to(instance, filename):
    base_name, ext = os.path.splitext(filename)
    hash_name = hashlib.md5(base_name).hexdigest()
    name = '%s%s' % (hash_name, ext)
    return os.path.join(os.path.join(UPLOAD_DIR + str(instance.bundle.id)), name)


def thumbnail_upload_to(instance, filename):
    base_name, ext = os.path.splitext(filename)
    hash_name = hashlib.md5(base_name).hexdigest()
    name = '%s%s' % (hash_name, ext)
    base_path = os.path.join(str(instance.bundle.id), name)
    return os.path.join(os.path.join(UPLOAD_DIR + 'thumbs'), base_path)

class ScreenshotManager(models.Manager):

    def ready(self):
        return self.get_query_set().filter(image__isnull=False)

class Screenshot(models.Model):
    bundle = models.ForeignKey('core.Bundle')
    url = models.CharField(max_length=1024)
    title = models.TextField(null=True)
    image = models.ImageField(null=True, upload_to=upload_to)
    thumbnail = models.ImageField(null=True, upload_to=thumbnail_upload_to)
    scheduled = models.DateTimeField(auto_now_add=True)
    saved = models.DateTimeField(null=True)

    def __unicode__(self):
        return u'Screenshot of %s' % self.url
    