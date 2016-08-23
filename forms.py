from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(required=True, max_length=100)
    search_by = forms.ChoiceField(choices=(("name", "Journal name"),
                                            ("issn", "ISSN"),
                                            ("cat", "Category (coming soon!)")))
    sort_by = forms.ChoiceField(choices=(("price", "APC (price)"),
                                         ("infl", "ArticleInfluence")))
    order = forms.ChoiceField(choices=(('asc', 'Ascending'),
                                       ('dsc', 'Descending')))

