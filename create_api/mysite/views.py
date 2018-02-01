# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from  mysite.models import Music
from  mysite.forms import PostForm
import boto
from boto.s3.key import Key
import os
import shutil
import json


# Create your views here.

def index(request):
    query_data = Music.objects.all()
    context = {"title":"All TAGS","Tag_name":query_data}
    return render(request, "home.html", context)


def tags_detail(request, id=None):
    instance = get_object_or_404(Music,id=id)
    file_url = get_file_url_from_s3(str(instance.title)+'/output.mp3')
    context = {"tag_name":instance.tag_name,
    "download_url":file_url,
    }
    return render(request, 'tag_detail.html', context)

def post_tags(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        file_name = Music.objects.get(title=instance.title)
        upload_files_to_s3('/home/ram/Documents/company_assignment/media_file/'+str(file_name.audio_file_name),
        str(instance.title)+'/output.mp3')
        shutil.rmtree('/home/ram/Documents/company_assignment/media_file/audio')
    context = {
        "form":form,
    }
    return render(request, "upload_file.html",context)

def get_bucket_name():
    AWS_CONNECTION = boto.connect_s3(os.environ['AWS_ACCESS_KEY_ID'],
                                 os.environ['AWS_SECRET_ACCESS_KEY'],host="s3.ap-south-1.amazonaws.com")
    bucket_name = AWS_CONNECTION.get_bucket("upload-audio-file")
    return bucket_name

def upload_files_to_s3(sys_file_path,s3_file_path):
    bucket_name = get_bucket_name()
    k = Key(bucket_name)
    k.key = s3_file_path
    k.set_contents_from_filename(sys_file_path)

def get_file_url_from_s3(s3_file_location):
    bucket = get_bucket_name()
    key = bucket.new_key(s3_file_location)
    file_url = key.generate_url(expires_in=600)
    return file_url


