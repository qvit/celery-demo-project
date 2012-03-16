# -*- coding: utf-8 -*-
from celery.task import task
from PIL import Image
from django.core.files import File
from selenium import webdriver
import datetime
import os
import tempfile

@task
def make_screenshot(screenshot):
    # get screenshot
    driver = webdriver.Firefox()
    driver.get(screenshot.url)
    fd, filename = tempfile.mkstemp('.png')
    os.close(fd)
    driver.save_screenshot(filename)
    driver.close()
    # save title, saved date and image
    screenshot.title = driver.title
    screenshot.saved = datetime.datetime.now()
    fileobj = File(open(filename))
    screenshot.image.save(filename, fileobj)
    # save thumbnail
    fd2, thumbnail_filename = tempfile.mkstemp('.png')
    os.close(fd2)
    image = Image.open(filename)
    cropped = image.crop((0, 0, 260*2, 180*2))
    cropped.thumbnail((260, 180), Image.ANTIALIAS)
    cropped.save(thumbnail_filename)
    fileobj = File(open(thumbnail_filename))
    screenshot.thumbnail.save(thumbnail_filename, fileobj)