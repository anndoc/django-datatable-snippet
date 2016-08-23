# -*- coding: utf-8 -*-
from django import forms


class BaseFilterForm(forms.Form):
    FIELDS = {}

    start = forms.IntegerField(initial=1)
    length = forms.IntegerField(initial=10)
    sort_asc = forms.ChoiceField(choices=(('', 'asc'), ('-', 'desc')), required=False)
    sort_column = forms.TypedChoiceField(coerce=int)
    search = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseFilterForm, self).__init__(*args, **kwargs)
        self.fields['sort_column'].choices = zip(map(str, range(len(self.FIELDS))), range(len(self.FIELDS)))

    def clean(self):
        cd = super().clean()
        cd['search'] = self.data.get('search[value]', '').lower()
        return cd
