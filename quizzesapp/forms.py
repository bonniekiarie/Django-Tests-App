from itertools import count
from django import forms
from .models import Test

class TestForm(forms.Form):
    tests = Test.objects.all()
    count = 0
    choices = []
    for test in tests:
        choice =(str(count), test.subject)
        choices.append(choice)
        count += 1
    Tests = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
        