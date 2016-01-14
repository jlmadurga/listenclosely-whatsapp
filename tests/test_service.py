#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from yowsup_celery.layer import CeleryLayer
from listenclosely_whatsapp.layer import ListenCloselyLayer
from yowsup.layers.logger.layer import YowLoggerLayer
try:
    from unittest import mock
except ImportError:
    import mock  # noqa
from django.conf import settings
settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
        }
    },
    ROOT_URLCONF="listenclosely.urls",
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "listenclosely_whatsapp",
    ],
    SITE_ID=1,
    MIDDLEWARE_CLASSES=(),
    LISTENCLOSELY_YOWSUP_NUMBER="341234567",
    LISTENCLOSELY_YOWSUP_PASS="password",
    LISTENCLOSELY_YOWSUP_TOP_LAYERS=('yowsup.layers.logger.layer.YowLoggerLayer',),
    LISTENCLOSELY_YOWSUP_ENCRYPTION=False
)

try:
    import django
    setup = django.setup
except AttributeError:
    pass
else:
    setup()


class TestService(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_caller_assigned(self):        
        caller = mock.MagicMock()
        from listenclosely_whatsapp.service import YowsupMessageServiceBackend
        service = YowsupMessageServiceBackend(caller)
        self.assertEqual(service.stack.caller, caller)
        
    def test_layer_order(self):
        caller = mock.MagicMock()
        from listenclosely_whatsapp.service import YowsupMessageServiceBackend
        service = YowsupMessageServiceBackend(caller)
        self.assertTrue(isinstance(service.stack.getLayer(6), YowLoggerLayer))
        self.assertTrue(isinstance(service.stack.getLayer(7), ListenCloselyLayer))
        self.assertTrue(isinstance(service.stack.getLayer(8), CeleryLayer))
