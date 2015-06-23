# -*- coding: utf-8 -*-
from livesettings import config_register, ConfigurationGroup, PositiveIntegerValue, PercentValue, StringValue
from django.utils.translation import ugettext_lazy as _

# First, setup a grup to hold all our possible configs
MYAPP_GROUP = ConfigurationGroup(
    'MyApp',               # key: internal name of the group to be created
    u'Настройки сайта',  # name: verbose name which can be automatically translated
    ordering=0             # ordering: order of group in the list (default is 1)
    )



config_register(StringValue(
                            MYAPP_GROUP,
        'EMAIL', 
        description = u'Email администратора',
        help_text = u"Почта, куда будут приходить заявки.",
        default = 'annkpx@gmail.com'
    ))

config_register(StringValue(
                            MYAPP_GROUP,
        'CONFERENCE_LINK',
        description = u'Ссылка на следующую конференцию',
        help_text = u"Ссылка, которая будет приходить людям при оплате конференции.",
        default = u'youtube.ru'
    ))
config_register(StringValue(
                            MYAPP_GROUP,
        'CONFERENCE_DATE',
        description = u'Дата следующей конференции',
        default = u''
    ))

config_register(PositiveIntegerValue(
                            MYAPP_GROUP,
        'CONFERENCE_PRICE',
        description = u'Сумма ёбаного якобы пожертвования на конереницию',
        help_text = u'с которого ты не платишь налоги',
        default = 1,
    ))
