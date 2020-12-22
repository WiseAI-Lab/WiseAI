from __future__ import unicode_literals

import logging

from django.db import models

# Get an instance of a logger
logger = logging.getLogger(__name__)


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-managed `created_at` and
    `modified_at` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = "base"
