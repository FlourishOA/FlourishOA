from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from django.db import models

@python_2_unicode_compatible
class Journal(models.Model):
    issn_number = models.CharField(max_length=9, primary_key=True)
    journal_name = models.CharField(max_length=150)
    article_influence = models.DecimalField(max_digits=8, decimal_places=5, null=True)
    est_article_influence = models.DecimalField(max_digits=8, decimal_places=5, null=True)
    is_hybrid = models.BooleanField()
    category = models.CharField(max_length=50, null=True)

    def __str__(self):
        result = self.issn_number + ": " + self.journal_name
        return result


@python_2_unicode_compatible
class Price(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    update_date = models.DateField()
    journal_issn = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return self.journal_issn + ": " + str(self.price) + "; " + str(self.update_date)

