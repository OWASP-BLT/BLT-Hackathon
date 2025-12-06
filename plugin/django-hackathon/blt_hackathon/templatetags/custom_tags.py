from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
from django.urls import reverse, NoReverseMatch
import os

register = template.Library()

@register.simple_tag
def static_url(path):
    """Simple static URL tag for compatibility"""
    return f"{settings.STATIC_URL}{path}"

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary"""
    if hasattr(dictionary, 'get'):
        return dictionary.get(key)
    return None

@register.simple_tag
def organization_exists():
    """Check if organization context exists - simplified for plugin"""
    return False  # Disable org-specific features in standalone plugin

@register.simple_tag(takes_context=True)
def get_org(context):
    """Get organization from context - simplified for plugin"""
    return None

@register.filter
def length_is(value, arg):
    """Check if length equals argument"""
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False

@register.simple_tag
def url_replace(request, field, value):
    """Replace URL parameter"""
    if hasattr(request, 'GET'):
        dict_ = request.GET.copy()
        dict_[field] = value
        return dict_.urlencode()
    return ""

@register.filter
def multiply(value, arg):
    """Multiply filter"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Divide filter"""
    try:
        return int(value) // int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.simple_tag
def get_setting(name, default=None):
    """Get a Django setting value"""
    return getattr(settings, name, default)

@register.filter
def addstr(arg1, arg2):
    """Concatenate two strings"""
    return str(arg1) + str(arg2)

@register.simple_tag
def url_exists(url_name, *args, **kwargs):
    """Check if a URL name exists"""
    try:
        reverse(url_name, args=args, kwargs=kwargs)
        return True
    except NoReverseMatch:
        return False

@register.filter
def truncate_chars(value, max_length):
    """Truncate string to specified length"""
    if len(str(value)) <= max_length:
        return value
    return str(value)[:max_length] + '...'

@register.simple_tag
def current_year():
    """Get current year"""
    from datetime import datetime
    return datetime.now().year

@register.filter
def default_if_none(value, default):
    """Return default if value is None"""
    return default if value is None else value

@register.simple_tag
def get_verbose_name(obj, field_name):
    """Get verbose name of a model field"""
    try:
        return obj._meta.get_field(field_name).verbose_name
    except:
        return field_name

@register.filter
def has_attr(obj, attr_name):
    """Check if object has attribute"""
    return hasattr(obj, attr_name)

@register.simple_tag(takes_context=True)
def active_page(context, *url_names):
    """Check if current page matches any of the given URL names"""
    request = context.get('request')
    if request and hasattr(request, 'resolver_match'):
        if request.resolver_match and request.resolver_match.url_name in url_names:
            return 'active'
    return ''