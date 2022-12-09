from django import template

register = template.Library()


@register.filter(name='rep_gmail')
def rep_gmail(value, args):
    return value.replace("@gmail", args)


@register.filter(name='get_reply')
def get_reply(dic, key):
    return dic.get(key)
