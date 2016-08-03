from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from api.models import Journal, Price, Influence
import json


class IndexView(TemplateView):
    template_name = "main_site/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['most_expensive'] = Price.objects.all().order_by('-price')[:5]
        context['num_journals'] = Journal.objects.all().count()
        context['num_prices'] = Price.objects.all().count()
        return context


class PriceAIView(TemplateView):
    template_name = "main_site/viz.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        price_ai_map = {}
        for i in Journal.objects.all().filter(article_influence__isnull=False):
           pass
        return context


class VisualizationView(TemplateView):
    template_name = 'main_site/viz.html'

    def get_context_data(self, **kwargs):
        context = super(VisualizationView, self).get_context_data(**kwargs)
        pairs = []
        for price_obj in Price.objects.all():
            try:
                ai = Influence.objects.get(journal__issn=price_obj.journal.issn,
                                           date_stamp__year=price_obj.date_stamp.year)
                pairs.append((float(price_obj.price), float(ai.article_influence)))

            except ObjectDoesNotExist:
                continue

        context['pairs'] = json.dumps(pairs)
        return context
