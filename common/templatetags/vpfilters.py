# coding: utf-8

from numbers import Number

from django import template

register = template.Library()


@register.filter
def subtract(lhs, rhs):
    rhs = int(rhs) if not isinstance(rhs, Number) else rhs
    lhs = int(lhs) if not isinstance(lhs, Number) else lhs
    return rhs - lhs

@register.filter
def divide(lhs, rhs):
    lhs = float(lhs) if not isinstance(lhs, Number) else lhs
    rhs = float(rhs) if not isinstance(rhs, Number) else rhs
    return lhs / rhs if rhs else None


@register.filter
def contains(enumeratable, obj):
    return obj in enumeratable


@register.filter
def split(value, separator=' '):
    return value.split(separator)
