# -*- coding: utf-8 -*-
import urlparse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django import forms
from shootr.core.models import Bundle, Screenshot
from shootr.core.tasks import make_screenshot


class ScreenshotForm(forms.Form):
    urls = forms.CharField(widget=forms.Textarea(attrs={'class': 'span12'}), label=u'Имена сайтов', )

    def clean_urls(self):
        urls = [
                self.clean_single_url(url) for url in \
                self.cleaned_data['urls'].strip().split()
        ]
        return urls

    def clean_single_url(self, url):
        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        if scheme != 'http':
            scheme = 'http'
        if not netloc:
            netloc, path = path, ''
        result = urlparse.urlunsplit((scheme, netloc, path, query, fragment))
        return result

    def save(self):
        bundle = Bundle.objects.create()
        for url in self.cleaned_data['urls']:
            shot = Screenshot.objects.create(bundle=bundle, url=url)
            make_screenshot.delay(shot)
        return bundle


def index(request):
    form = ScreenshotForm(request.POST or None)
    if form.is_valid():
        bundle = form.save()
        return redirect('get_bundle', bundle.id)
    return render_to_response('core/index.html', {'form': form})


def get_bundle(request, bundle_id):
    bundle = get_object_or_404(Bundle, pk=bundle_id)
    return render_to_response('core/get_bundle.html', {'bundle': bundle})