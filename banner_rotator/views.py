"""Banner Rotator views."""
# -*- coding:utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render

from banner_rotator.models import Banner, Place


def click(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    banner.click(request)

    return redirect(banner.url)


def banner_for(request, place_slug):
    place = get_object_or_404(Place, slug=place_slug)

    try:
        banner = Banner.objects.biased_choice(place)
        banner.view()
    except Banner.DoesNotExist:
        raise Http404

    content_type = request.META.get("CONTENT_TYPE", 'text/plain')

    if 'application/json' in content_type:
        return HttpResponse(json.dumps({
            'banner': {
                'id': banner.id,
                'name': banner.name,
                'url_target': banner.url_target,
                'url': reverse('banner_click', args=[banner.id]),
                'file': banner.file.url,
                'alt': banner.alt,
                'is_swf': banner.is_swf()
            },
            'place': {
                'name': place.name,
                'slug': place.slug,
                'width': place.width,
                'height': place.height
            }
        }), content_type="application/json")

    return render(request, 'banner_rotator/place.html', {
        'banner': banner,
        'banner_place': place,
        'iframe': True
    })
