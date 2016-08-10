from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from api.models import Journal, Price, Influence
from api.serializers import JournalSerializer, PriceSerializer, InfluenceSerializer
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
        context = super(PriceAIView, self).get_context_data(**kwargs)
        price_ai_map = {}
        for i in Journal.objects.all().filter(article_influence__isnull=False):
           pass
        return context


class VisualizationView(TemplateView):
    template_name = 'main_site/viz.html'

    def get_context_data(self, **kwargs):
        context = super(VisualizationView, self).get_context_data(**kwargs)
        events = []
        for price in Price.objects.filter(influence__isnull=False):
            event = PriceSerializer(price).data
            event.update(JournalSerializer(price.journal))
            event['article_influence'] = price.influence.article_influence
            event['est_article_influence'] = price.influence.est_article_influence
            events.append(event)

        context['events'] = json.dumps(events)
        print len(events)
        return context
