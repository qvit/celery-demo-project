# -*- coding: utf-8 -*-
import urlparse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django import forms
from shootr.core.models import Bundle, Screenshot
from shootr.core.tasks import make_screenshot


class ScreenshotForm(forms.Form):
    urls = forms.CharField(widget=forms.Textarea(attrs={'class': 'span12'}), label=u'Адреса сайтов', )

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
    bundle_list = []
    bundle_no = 1
    bundle_key = 'bundle%d' % bundle_no
    while bundle_key in request.POST:
        bundle_list.append(Bundle.objects.get(id=request.POST.get(bundle_key)))
        bundle_no += 1
        bundle_key = 'bundle%d' % bundle_no
    if form.is_valid():
        bundle = form.save()
        bundle_list.append(bundle)
        form = ScreenshotForm()
    return render_to_response('core/index.html', {'form': form, 'bundle_list': bundle_list})


def get_bundle(request, bundle_id):
    bundle = get_object_or_404(Bundle, pk=bundle_id)
    return render_to_response('core/get_bundle.html', {'bundle': bundle})