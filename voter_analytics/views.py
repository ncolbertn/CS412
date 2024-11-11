from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.db import models
import plotly.express as px
from plotly.io import to_html
from .models import Voter
from .forms import VoterFilterForm

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100


    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            # Party affiliation filter
            party = form.cleaned_data.get('party_affiliation')
            if party:
                queryset = queryset.filter(party_affiliation=party)

            # Date of birth range filter
            min_dob = form.cleaned_data.get('min_date_of_birth')
            max_dob = form.cleaned_data.get('max_date_of_birth')
            if min_dob:
                queryset = queryset.filter(date_of_birth__gte=min_dob)
            if max_dob:
                queryset = queryset.filter(date_of_birth__lte=max_dob)

            # Voter score filter
            voter_score = form.cleaned_data.get('voter_score')
            if voter_score != '':
                queryset = queryset.filter(voter_score=voter_score)

            # Specific elections filters
            elections = [
                ('v20state', form.cleaned_data.get('v20state')),
                ('v21town', form.cleaned_data.get('v21town')),
                ('v21primary', form.cleaned_data.get('v21primary')),
                ('v22general', form.cleaned_data.get('v22general')),
                ('v23town', form.cleaned_data.get('v23town'))
            ]
            for field, voted in elections:
                if voted:
                    queryset = queryset.filter(**{field:True})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)  # Pass form to template
        return context
    

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter' 


class VoterGraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    
    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        
        if form.is_valid():
            party = form.cleaned_data.get('party_affiliation')
            min_dob = form.cleaned_data.get('min_date_of_birth')
            max_dob = form.cleaned_data.get('max_date_of_birth')
            voter_score = form.cleaned_data.get('voter_score')

            if party:
                queryset = queryset.filter(party_affiliation=party)
            if min_dob:
                queryset = queryset.filter(date_of_birth__year__gte=min_dob)
            if max_dob:
                queryset = queryset.filter(date_of_birth__year__lte=max_dob)
            if voter_score:
                queryset = queryset.filter(voter_score=voter_score)

            # Election participation filters
            elections = [
                ('v20state', form.cleaned_data.get('v20state')),
                ('v21town', form.cleaned_data.get('v21town')),
                ('v21primary', form.cleaned_data.get('v21primary')),
                ('v22general', form.cleaned_data.get('v22general')),
                ('v23town', form.cleaned_data.get('v23town'))
            ]
            for field, voted in elections:
                if voted:
                    queryset = queryset.filter(**{field: True})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        #Distribution by Year of Birth
        birth_years = queryset.values_list('date_of_birth', flat=True)
        years = [dob.year for dob in birth_years]
        fig1 = px.histogram(x=years, nbins=30, title="Distribution of Voters by Year of Birth")
        fig1.update_layout(xaxis_title="Year of Birth", yaxis_title="Count of Voters")
        context['birth_year_histogram'] = to_html(fig1, full_html=False)

        # Party Affiliation Distribution
        party_counts = queryset.values('party_affiliation').annotate(count=models.Count('party_affiliation'))
        fig2 = px.pie(party_counts, names='party_affiliation', values='count', title="Distribution of Voters by Party Affiliation")
        context['party_pie_chart'] = to_html(fig2, full_html=False)

        #Participation in Elections
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        participation_counts = {field: queryset.filter(**{field: True}).count() for field in election_fields}
        fig3 = px.bar(x=list(participation_counts.keys()), y=list(participation_counts.values()), title="Voter Participation in Elections")
        fig3.update_layout(xaxis_title="Election", yaxis_title="Count of Voters")
        context['election_participation_histogram'] = to_html(fig3, full_html=False)
        context['form'] = VoterFilterForm(self.request.GET)

        return context