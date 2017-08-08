from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from choices import LICENSES, CURRENCIES

@python_2_unicode_compatible
class Journal(models.Model):
    """
    Model of a journal, with the ISSN as the primary key of the model
    """
    issn = models.CharField(max_length=9, primary_key=True)
    journal_name = models.CharField(max_length=150)
    pub_name = models.CharField(max_length=150)
    is_hybrid = models.BooleanField()
    category = models.CharField(max_length=50, null=True)
    url = models.CharField(max_length=300, null=True)

    def __str__(self):
        result = self.issn + ": " + self.journal_name
        return result


@python_2_unicode_compatible
class Influence(models.Model):
    article_influence = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    est_article_influence = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    ai_percentile = models.DecimalField(max_digits=10, decimal_places=10, null=True)
    eigenfactor = models.DecimalField(max_digits=10, decimal_places=10, null=True)
    ef_percentile = models.DecimalField(max_digits=10, decimal_places=10, null=True)
    efn = models.DecimalField(max_digits=10, decimal_places=10, null=True)
    cost_effectiveness = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    date_stamp = models.DateField()
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return (self.journal.issn + ": " + str(self.date_stamp) + "," +
                str(self.article_influence) if self.article_influence else str(self.est_article_influence) + ";")


@python_2_unicode_compatible
class Price(models.Model):
    """
    Model of a single price 'event'; there may be multiple price events
    for each journal. One journal may map to many price events
    """

    price = models.DecimalField(max_digits=7, decimal_places=2)
    date_stamp = models.DateField()
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    influence = models.ForeignKey(Influence, null=True, on_delete=models.SET_NULL)
    url = models.CharField(max_length=300, null=True)
    license = models.CharField(max_length=30, choices=LICENSES)

    def __str__(self):
        result = self.journal.issn + ": "
        if self.influence:
            if self.influence.article_influence:
                result += str(self.influence.article_influence)
            elif self.influence.est_article_influence:
                result += "(est) " + str(self.influence.est_article_influence)
            else:
                result += "No influence value"
        else:
            result += "No influence value"
        result += " - " + str(self.date_stamp)
        return result

@python_2_unicode_compatible
class UserSubmission(models.Model):
    class Meta:
        db_table = 'user_submissions'

    issn = models.CharField(max_length=9)
    date_stamp = models.DateField()
    journal_name = models.CharField(max_length=150)
    pub_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    currency = models.CharField(max_length=20, choices=CURRENCIES)
    url = models.CharField(max_length=150)
    comment = models.CharField(max_length=150)

    def __str__(self):
        return "this is a placeholder"

