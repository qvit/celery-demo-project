# -*- coding: utf-8 -*-
from celery.task import task
from PIL import Image
from django.core.files import File
from selenium import webdriver
import datetime
import os
import tempfile

fileformat = '.png'
thumb_width = 260
thumb_height = 180

@task
def make_screenshot(screenshot):
    shot = get_screenshot(screenshot)
    screenshot.image.save(shot.name, shot)
    thumb = make_thumbnail(shot)
    screenshot.thumbnail.save(thumb.name, thumb)

def get_screenshot(screenshot):
    driver = webdriver.Firefox()
    driver.get(screenshot.url)
    fd, filename = tempfile.mkstemp(fileformat)
    os.close(fd)
    driver.save_screenshot(filename)
    driver.close()
    screenshot.title = driver.title
    screenshot.saved = datetime.datetime.now()
    return File(open(filename))

def make_thumbnail(shot):
    fd, thumbnail_filename = tempfile.mkstemp(fileformat)
    os.close(fd)
    image = Image.open(shot.name)
    cropped = image.crop((0, 0, thumb_width*2, thumb_height*2))
    cropped.thumbnail((thumb_width, thumb_height), Image.ANTIALIAS)
    cropped.save(thumbnail_filename)
    return File(open(thumbnail_filename))
