from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from django.db import models

@python_2_unicode_compatible
class Journal(models.Model):
    """
    Model of a journal, with the ISSN as the primary key of the model
    """
    issn = models.CharField(max_length=9, primary_key=True)
    journal_name = models.CharField(max_length=150)

    def __str__(self):
        result = self.issn + ": " + self.journal_name
        return result


@python_2_unicode_compatible
class Price(models.Model):
    """
    Model of a single price 'event'; there may be multiple price events
    for each journal. One journal may map to many price events
    """
    price = models.DecimalField(max_digits=7, decimal_places=2)
    date_stamp = models.DateField()
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return self.journal.issn + ": " + str(self.price) + ", " \
               + str(self.date_stamp) + ";"


@python_2_unicode_compatible
class Influence(models.Model):
    article_influence = models.DecimalField(max_digits=8, decimal_places=5, null=True)
    est_article_influence = models.DecimalField(max_digits=8, decimal_places=5, null=True)
    date_stamp = models.DateField()
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return self.journal.issn + ": " + str(self.article_influence) + ":OR:"\
               + str(self.est_article_influence) + ", " + str(self.date_stamp) + ";"


@python_2_unicode_compatible
class Type(models.Model):
    is_hybrid = models.BooleanField()
    date_stamp = models.DateField()
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return self.journal.issn + ": " + str(self.is_hybrid) + ", " \
               + str(self.date_stamp) + ";"


@python_2_unicode_compatible
class Category(models.Model):
    category = models.CharField(max_length=50, null=True)
    date_stamp = models.DateField()
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return self.journal.issn + ": " + str(self.category) + ", " \
               + str(self.date_stamp) + ";"


@python_2_unicode_compatible
class Publisher(models.Model):
    pub_name = models.CharField(max_length=150)
    date_stamp = models.DateField()
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return self.journal.issn + ": " + str(self.pub_name) + ", " \
               + str(self.date_stamp) + ";"

