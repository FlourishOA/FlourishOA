from django.shortcuts import render
from django.views.generic import TemplateView
from api.models import Journal, PriceInfluence


class IndexView(TemplateView):
    template_name = "main_site/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['most_expensive'] = PriceInfluence.objects.all().order_by('-price')[:5]
        context['num_journals'] = Journal.objects.all().count()
        context['num_prices'] = PriceInfluence.objects.all().count()
        return context

class PriceAIView(TemplateView):
    template_name = "main_site/viz.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        price_ai_map = {}
        for i in Journal.objects.all().filter(article_influence__isnull=False):
           pass
        return context
