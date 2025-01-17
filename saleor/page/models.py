from django.db import models
from django.utils.translation import pgettext_lazy
from draftjs_sanitizer import clean_draft_js

from ..core.db.fields import SanitizedJSONField
from ..core.models import PublishableModel, PublishedQuerySet
from ..core.utils.translations import TranslationProxy
from ..seo.models import SeoModel, SeoModelTranslation


class PagePublishedQuerySet(PublishedQuerySet):
    @staticmethod
    def user_has_access_to_all(user):
        return user.is_active and user.has_perm("page.manage_pages")


class Page(SeoModel, PublishableModel):
    slug = models.SlugField(unique=True, max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    content_json = SanitizedJSONField(
        blank=True, default=dict, sanitizer=clean_draft_js
    )
    created = models.DateTimeField(auto_now_add=True)

    objects = PagePublishedQuerySet.as_manager()
    translated = TranslationProxy()

    class Meta:
        ordering = ("slug",)
        permissions = (
            ("manage_pages", pgettext_lazy("Permission description", "Manage pages.")),
        )

    def __str__(self):
        return self.title

    # Deprecated. To remove in #5022
    @staticmethod
    def get_absolute_url():
        return ""


class PageTranslation(SeoModelTranslation):
    language_code = models.CharField(max_length=10)
    page = models.ForeignKey(
        Page, related_name="translations", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    content_json = SanitizedJSONField(
        blank=True, default=dict, sanitizer=clean_draft_js
    )

    class Meta:
        unique_together = (("language_code", "page"),)

    def __repr__(self):
        class_ = type(self)
        return "%s(pk=%r, title=%r, page_pk=%r)" % (
            class_.__name__,
            self.pk,
            self.title,
            self.page_id,
        )

    def __str__(self):
        return self.title
