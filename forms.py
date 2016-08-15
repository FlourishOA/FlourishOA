from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(label="Enter query:", max_length=100)
