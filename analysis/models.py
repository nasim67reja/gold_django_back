from django.db import models

class PriceData(models.Model):
    time = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    ema = models.FloatField(null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.time)
