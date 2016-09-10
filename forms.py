from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(required=True, max_length=100)
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

