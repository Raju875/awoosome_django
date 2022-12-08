from django.db import models


class SessionCookieCache(models.Model):

    class Meta:

        managed = False  # No database table creation or deletion  \
        # operations will be performed for this model.

        # default_permissions = ()  # disable "add", "change", "delete"
        # and "view" default permissions

        permissions = (
            ("change_session_cookie_cache_status", "Can change the status of session-cookie-cache"),
        )
