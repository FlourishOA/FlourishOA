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
        context['most_expensive'] = Price.objects.all().order_by('-price')[:5]
        context['num_journals'] = Journal.objects.all().count()
        context['num_prices'] = Price.objects.all().count()
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

    def get(self, request, **kwargs):
        form = SearchForm(request.GET)
        if form.is_valid():
            results = []

            # figuring out which field to filter on
            search_by_raw = form.cleaned_data['search_by']
            if search_by_raw == 'Category':
                search_by = 'category__contains'
            elif search_by_raw == 'ISSN':
                search_by = 'issn__contains'
            else:
                search_by = 'journal_name__contains'

            # passing correct kwarg to filter
            for journal in Journal.objects.filter(**{search_by: form.cleaned_data['search_query']}):
                results.append(journal)
            return render(request, 'main_site/search.html', {'form': form, 'results': results})
        return render(request, 'main_site/search.html', {'form': form})


class ResultView(TemplateView):
    template_name = 'main_site/result.html'

    def get(self, request, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)
        context['journal'] = Journal.objects.get(issn=kwargs['issn'])
        context['prices'] = Price.objects.filter(journal__issn=kwargs['issn'])
        return render(request, 'main_site/result.html', context)
