from django.template.defaulttags import register
import datetime

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
@register.filter
def multiply(value, arg):
	return value * arg
@register.filter
def roundten(value):
	ten = value/10
	ten = int(round(ten))
	ten = ten * 10
	return ten


@register.filter
def less_now(value):
	now = datetime.datetime.now().date()
	if value.date() < now:
		return True
	else:
		return False

@register.filter
def decToPoint(value):
	a = str(value)
	a = a.replace(',', '.')
	return a
