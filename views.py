from django.views.generic import TemplateView
from django.shortcuts import render
from api.models import Journal, Price, Influence
from django.http import HttpResponseRedirect
from api.serializers import JournalSerializer, PriceSerializer, InfluenceSerializer
from main_site.forms import SearchForm
import simplejson as json


class IndexView(TemplateView):
    template_name = "main_site/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # finding the date of the most recent update
        context['most_recent_update'] = max([
            Price.objects.all().order_by('-date_stamp')[0].date_stamp,
            Influence.objects.all().order_by('-date_stamp')[0].date_stamp,
        ]).strftime("%m/%d/%y")
        context['most_expensive'] = Price.objects.all().order_by('-price')[:5]
        context['num_journals'] = Journal.objects.all().count()
        context['num_prices'] = Price.objects.all().count()
        context['num_influences'] = Influence.objects.all().count()

        return context


class VisualizationView(TemplateView):
    template_name = 'main_site/viz.html'

    def get_context_data(self, **kwargs):
        context = super(VisualizationView, self).get_context_data(**kwargs)

        events = []

        valid_prices = Price.objects.filter(influence__article_influence__isnull=False,
                                            date_stamp__year__gte=2012)
        for price in valid_prices:
            event = PriceSerializer(price).data
            event.update(JournalSerializer(price.journal).data)
            event["article_influence"] = price.influence.article_influence
            event["est_article_influence"] = price.influence.est_article_influence
            events.append(event)

        context['events'] = json.dumps(events)
        context['num_valid_pairs'] = valid_prices.count()

        return context


class SearchView(TemplateView):
    template_name = 'main_site/search.html'

    @staticmethod
    def _reorder(cleaned_data, results):
        # ^^ okay so there are our results now its just a matter of ordering them correctly

        # figuring out which direction to order the results
        rev = True if cleaned_data['order'] == "dsc" else False # default to ascending

        def sort_on(result):
            # figuring out which field to sort on
            sort_by_raw = cleaned_data['sort_by']
            if sort_by_raw == 'price':
                return result['mrp'].price
            elif sort_by_raw == 'infl':
                mri = result['mri']
                if mri:
                    return mri.article_influence
                else:
                    return 0
            else:  # default to alphabetical order
                return result['journal'].journal_name

        return sorted(results, reverse=rev, key=sort_on)

    @staticmethod
    def _get_mrp(journal):
        """
        Getting mrp (most recent price)

        Returns None if no price exists
        """
        try:
            return Price.objects.filter(journal__issn=journal.issn).order_by('-date_stamp')[0]
        except IndexError:
            return None

    @staticmethod
    def _get_mri(journal):
        """
        Getting mri (most recent influence)

        Returns 0 if no influence exists
        """
        try:
            return Influence.objects.filter(journal__issn=journal.issn).order_by('-date_stamp')[0]
        except IndexError:
            return 0

    @staticmethod
    def _get_results(cleaned_data):
        # figuring out which field to filter on
        search_by_raw = cleaned_data['search_by']
        if search_by_raw == 'cat':
            search_by = 'category__icontains'
        elif search_by_raw == 'issn':
            search_by = 'issn__icontains'
        else:  # default to the journal name
            search_by = 'journal_name__icontains'

        return [{'journal': result, 'mrp': SearchView._get_mrp(result), 'mri': SearchView._get_mri(result)}
                for result in Journal.objects.filter(**{search_by: cleaned_data['search_query']})]

    def get(self, request, **kwargs):
        form = SearchForm(request.GET)
        if form.is_valid():
            results = self._reorder(form.cleaned_data, self._get_results(form.cleaned_data))

            return render(request, 'main_site/search.html', {'form': form, 'results': results})
        return render(request, 'main_site/search.html', {'form': form})


class ResultView(TemplateView):
    template_name = 'main_site/result.html'

    def get(self, request, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)
        context['journal'] = Journal.objects.get(issn=kwargs['issn'])
        context['prices'] = Price.objects.filter(journal__issn=kwargs['issn'])
        infl_set = Influence.objects.filter(journal__issn=kwargs['issn'])
        context['has_influence'] = infl_set.exists()
        context['influences'] = infl_set
        return render(request, 'main_site/result.html', context)
