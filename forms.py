from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(required=True, max_length=100)
    search_by = forms.ChoiceField(choices=(("Journal name", "Journal name"),
                                            ("ISSN", "ISSN"),
                                            ("Category", "Category")))