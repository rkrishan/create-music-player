# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Music(models.Model):
    title = models.CharField(max_length=120,unique=True)
    tag_name = models.CharField(max_length=120)
    audio_file_name = models.FileField(upload_to='audio/%Y/%m/%d')


    def __unicode__(self):
        return self.tag_name 