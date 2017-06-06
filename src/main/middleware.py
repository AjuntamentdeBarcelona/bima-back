# -*- coding: utf-8 -*-
from django.conf import settings


def force_default_language_middleware(get_response):
    """
    Change Accept-Language HTTP headers

    This will force the I18N machinery unless another one is set via sessions or cookies

    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        ui_language = getattr(settings, 'INTERFACE_LANGUAGE_CODE', None)
        if ui_language and 'HTTP_ACCEPT_LANGUAGE' in request.META:
            request.META['HTTP_ACCEPT_LANGUAGE'] = ui_language

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
