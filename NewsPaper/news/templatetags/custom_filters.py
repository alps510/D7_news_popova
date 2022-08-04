from django import template

register = template.Library()
check_list = ['технологии', 'Alder', 'подход', 'навык', 'правильно']


@register.filter()
def censor(value):
    content_list = value.split()
    new_content_list = ''
    for i in content_list:
        for j in range(len(check_list)):
            if i == check_list[j]:
                i = i[0] + '*' * (len(i) - 1)
        new_content_list += i + ' '
    return f'{new_content_list}'
