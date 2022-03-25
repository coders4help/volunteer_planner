# coding: utf-8

from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row

register = template.Library()


@register.inclusion_tag(
    "admin/scheduletemplates/scheduletemplate/scheduletemplate_submit_line.html",
    takes_context=True,
)
def schedule_template_submit_row(context):
    return submit_row(context)
