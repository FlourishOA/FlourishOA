from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from django.db import models

@python_2_unicode_compatible
class Journal(models.Model):
    """
    Model of a journal, with the ISSN as the primary key of the model
    """
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
    """
    Model of a single price 'event'; there may be multiple price events
    for each journal. One journal may map to many price events
    """
    price = models.DecimalField(max_digits=7, decimal_places=2)
    time_stamp = models.DateTimeField()
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return self.journal.issn_number + ": " + str(self.price) + ", " \
               + str(self.time_stamp) + ";"

@python_2_unicode_compatible
class Publisher(models.Model):
    """
    Model of a publisher. One publisher may map to many journals,
    which are listed by ISSN (a foreign key)
    """
    publisher_name = models.CharField(max_length=150)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return self.publisher_name + ": " + self.journal.issn_number


