import json

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django.conf.urls import url
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from . import models
from . import forms

class ImageAdminInline(GenericInlineModelAdmin):
    model = models.Image
    form = forms.ImageAdminInlineForm
    template = "gallery/edit_inline/image_admin.html"
    extra = 0

    class Media:
        js = (
            "/static/admin/js/jquery-ui.js",
            "/static/js/content-gallery-helpers.js",
            "/static/admin/js/content-gallery-admin-view.js",
            "/static/admin/js/inline_admin.js",
        )
        css = {
            "all": ("/static/admin/css/inline_admin.css",)
        }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('position')


class ImageAdmin(admin.ModelAdmin):
    form = forms.ImageAdminForm

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            url(
                r'^ajax/preview/(?P<pk>\d+)/$',
                self.preview,
                name='gallery_new_image_preview'
            ),
        ]
        return extra_urls + urls

    def preview(self, request, pk):
        image = get_object_or_404(models.Image, pk=pk)
        response = {
            "preview_url": image.preview_url,
            "position": image.position,
        }
        return HttpResponse(json.dumps(response), content_type='application/json')

admin.site.register(models.Image, ImageAdmin)
