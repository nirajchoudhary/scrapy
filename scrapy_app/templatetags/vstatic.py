import os
from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag(name="vstatic")
def vstatic(path):
    """
        Return absolute URL to static file with versioning.
    """
    url = os.path.join(settings.STATIC_URL, path)
    version = settings.STATIC_VERSION

    try:
        if version == 'mtime':
            full_path = os.path.join(settings.BASE_DIR,
                                     settings.STATIC_DIR, path)
            version = int(os.path.getmtime(full_path))

        if '?' in url:
            url = '{0}&v={1}'.format(url, version)
        else:
            url = '{0}?v={1}'.format(url, version)
    except Exception as e:
        print e
    return url
