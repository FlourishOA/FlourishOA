from django import forms
from api.models import Journal
from dal import autocomplete

class SearchForm(forms.Form):
    search_query = forms.CharField(required=True,max_length=150)
    sort_by = forms.ChoiceField(choices=(("ce", "Cost Effectiveness"),
                                         ("alpha", "Alphabetical"),
                                         ("price", "APC (price)"),
                                         ("infl", "ArticleInfluence")))
    search_by = forms.ChoiceField(choices=(("name", "Journal name"),
                                           ("pub", "Publisher"),
                                           ("issn", "ISSN"),
                                           ("cat", "Category")))
    order = forms.ChoiceField(choices=(('dsc', 'Descending'),
                                       ('asc', 'Ascending')))


class JournalNameSearchForm(forms.Form):
    search_query = forms.ModelChoiceField(required=True,
                                          queryset=Journal.objects.all(),
                                          widget=autocomplete.ModelSelect2(url='journal-autocomplete'),
                                          )

    search_by = forms.ChoiceField(choices=(("name", "Journal name"),
                                       ("pub", "Publisher"),
                                       ("issn", "ISSN"),
                                       ("cat", "Category")))
    sort_by = forms.ChoiceField(choices=(("ce", "Cost Effectiveness"),
                                         ("alpha", "Alphabetical"),
                                         ("price", "APC (price)"),
                                         ("infl", "ArticleInfluence")))


    order = forms.ChoiceField(choices=(('dsc', 'Descending'),
                                   ('asc', 'Ascending')))

class CategorySearchForm(SearchForm):
    search_query = forms.ModelChoiceField(required=True,
                                          queryset=Journal.objects.all(),
                                          widget=autocomplete.ModelSelect2(url='journal-autocomplete'))
    search_by = forms.ChoiceField(choices=(("cat", "Category"),
                                           ("name", "Journal name"),
                                           ("pub", "Publisher"),
                                           ("issn", "ISSN")))