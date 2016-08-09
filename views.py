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
        context = super(TemplateView, self).get_context_data(**kwargs)
        price_ai_map = {}
        for i in Journal.objects.all().filter(article_influence__isnull=False):
           pass
        return context


class VisualizationView(TemplateView):
    template_name = 'main_site/viz.html'

    def get_context_data(self, **kwargs):
        context = super(VisualizationView, self).get_context_data(**kwargs)
        events = []
        for price_obj in Price.objects.all():
            try:
                ai_list = Influence.objects.filter(journal__issn=price_obj.journal.issn,
                                                   date_stamp__year=price_obj.date_stamp.year)\
                                                   .order_by('date_stamp')
                if ai_list:
                    event = {}
                    ai = ai_list[0]
                    ai_ser = InfluenceSerializer(ai)
                    price_ser = PriceSerializer(price_obj)
                    journal_ser = JournalSerializer(ai.journal)
                    event['ai'] = ai_ser.data['article_influence']
                    event['ai_date_stamp'] = ai_ser.data['date_stamp']
                    event['price'] = price_ser.data['price']
                    event['price_date_stamp'] = price_ser.data['date_stamp']
                    event.update(journal_ser.data)
                    events.append(event)

            except ObjectDoesNotExist:
                continue

        context['events'] = json.dumps(events)
        print len(events)
        return context
