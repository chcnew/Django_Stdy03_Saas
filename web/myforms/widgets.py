# -*- coding:utf-8 -*-
from django.forms.widgets import RadioSelect
from django.forms.widgets import Select


class ColorRadioSelect(RadioSelect):
    # template_name = 'django/forms/widgets/radio.html'
    # option_template_name = 'django/forms/widgets/radio_option.html'
    template_name = 'web/widgets/color_radio/radio.html'
    option_template_name = 'web/widgets/color_radio/radio_option.html'


class ColorSelect(Select):
    # template_name = "django/forms/widgets/select.html"
    # option_template_name = "django/forms/widgets/select_option.html"
    template_name = "web/widgets/color_select/select.html"
    option_template_name = "web/widgets/color_select/select_option.html"
