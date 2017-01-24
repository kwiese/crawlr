from django import forms

class ApplicationForm(forms.Form):
    start_address = forms.CharField(label='start_address', max_length=200, required=True)
    budget = forms.ChoiceField(label='budget', required=True)
    search_radius = forms.DecimalField(label='search_radius',max_value=5000.0, decimal_places=2, required=True)
    user_time = forms.CharField(label='user_time',max_length=5, required=True)
