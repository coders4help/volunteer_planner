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


@register.filter
def eq(lhs, rhs):
    return lhs == rhs


@register.filter
def neq(lhs, rhs):
    return lhs != rhs


@register.filter
def yes(lhs, rhs, default=""):
    return rhs if lhs else default


@register.filter
def no(lhs, rhs, default=""):
    return rhs if not lhs else default


@register.filter
def get(obj, key):
    return obj[key]
