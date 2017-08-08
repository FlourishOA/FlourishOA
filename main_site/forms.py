from django import forms
from api.models import Journal
from dal import autocomplete
from choices import LICENSES
from datetime import date


class SearchForm(forms.Form):
    search_query = forms.CharField(required=True, max_length=150)
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


class JournalInfoForm(forms.Form):
    issn = forms.CharField(label='ISSN', max_length=9)
    journal_name = forms.CharField(label='Journal name', max_length=150)
    pub_name = forms.CharField(label='Publisher name', max_length=150)
    is_hybrid = forms.BooleanField(label='Journal is a hybrid', required=False)
    category = forms.CharField(label='Category', max_length=50, required=False)
    url = forms.CharField(label='URL of info', max_length=300, required=False)


class PriceInfoForm(forms.Form):
    journal_id = forms.CharField(label='ISSN', max_length=9)
    price = forms.DecimalField(max_digits=7, decimal_places=2)
    date_stamp = forms.DateField(label='Today\'s date (YYYY-MM-DD)')
    url = forms.CharField(label='URL of info', max_length=300, required=False)
    license = forms.ChoiceField(choices=LICENSES, initial=10)


class SubmitInfoForm(forms.Form):
    issn = forms.CharField(label='ISSN', max_length=9, required=False)
    date_stamp = forms.DateField(label='Date of Price/Submission (YYYY-MM-DD)', input_formats=['%Y-%m-%d'], required=True)
    journal_name = forms.CharField(label='Journal name (required)', max_length=150)
    pub_name = forms.CharField(label='Publisher name', max_length=150, required=False)
    price = forms.DecimalField(max_digits=7, decimal_places=2, required=False)
    currency = forms.ChoiceField(label="Currency (required if price provided)", choices=(('none', "Select Currency"),
                                 ('usd', 'USD'),
                                 ('euro', 'EURO'),
                                 ('yen', 'YEN'),
                                 ('pound', 'POUND'),
                                 ('franc', 'FRANC'),
                                 ('yuan', 'YUAN'),
                                 ('other', 'OTHER')))
    url = forms.CharField(label='Url', max_length=150, required=False)
    comment = forms.CharField(label='Additional Information', max_length=150, required=False)

