from django.conf import settings as django_settings


def site_settings(request):
    return {
        "SITE_NAME": getattr(django_settings, "WAGTAIL_SITE_NAME", ""),
    }
