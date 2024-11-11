from django import forms
from .models import Voter
import datetime

class VoterFilterForm(forms.Form):
    # Party affiliation
    party_affiliation = forms.ChoiceField(
        choices=[('', 'All')] + [(party, party) for party in Voter.objects.values_list('party_affiliation', flat=True).distinct()],
        required=False
    )

    # Date of birth range (min and max)
    year_choices = [(datetime.datetime.strptime((str(year) + '-01-01'), '%Y-%m-%d').date(), year) for year in range(1920, datetime.date.today().year + 1)]
    min_date_of_birth = forms.ChoiceField(choices=[('', 'No Minimum')] + year_choices, required=False)
    max_date_of_birth = forms.ChoiceField(choices=[('', 'No Maximum')] + year_choices, required=False)

    # Voter score
    voter_score = forms.ChoiceField(
        choices=[('', 'Any')] + [(i, i) for i in range(6)],  # 0-5 for the past 5 elections
        required=False
    )

    # Specific election participation
    v20state = forms.BooleanField(required=False, label='2020 State Election')
    v21town = forms.BooleanField(required=False, label='2021 Town Election')
    v21primary = forms.BooleanField(required=False, label='2021 Primary Election')
    v22general = forms.BooleanField(required=False, label='2022 General Election')
    v23town = forms.BooleanField(required=False, label='2023 Town Election')
