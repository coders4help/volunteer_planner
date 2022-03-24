# coding: utf-8
from django.conf import settings

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from . import models, forms


class FlatPageStyleInline(admin.StackedInline):
    model = models.FlatPageExtraStyle
    verbose_name = _('additional CSS')
    verbose_name_plural = _('additional CSS')
    template = 'flatpages/additional_flat_page_style_inline.html'


class FlatPageTranslationInline(admin.StackedInline):
    model = models.FlatPageTranslation
    form = forms.FlatPageTranslationFormWithHTMLEditor
    verbose_name = _('translation')
    verbose_name_plural = _('translations')
    extra = 0


class FlatPageTranslationAdmin(FlatPageAdmin):
    inlines = [
        FlatPageStyleInline,
        FlatPageTranslationInline,
    ]

    form = forms.FlatPageFormWithHTMLEditor
    list_filter = ('sites', 'registration_required',)
    list_display = (
        'title',
        'url',
        'registration_required',
        'get_translations',
    )
    search_fields = ('url', 'title')

    def get_translations(self, obj):
        translations = list(obj.translations.all())
        trans_list = None
        if translations:
            translations = sorted(
                t.get_language_display() for t in translations)

            trans_list = u'<ul>{}</ul>'.format(
                u'\n'.join(u'<li>{}</li>'.format(t) for t in translations)
            )
        return format_html(
            u'{}/{}:<br />{}'.format(
                len(translations),
                len(settings.LANGUAGES),
                trans_list or _('No translation available')
            )
        )

    get_translations.allow_tags = True
    get_translations.short_description = _('translations')


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageTranslationAdmin)
