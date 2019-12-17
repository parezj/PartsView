from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.models import User
from jsonfield import JSONField

class BasePart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    name_enc = models.CharField(default="", max_length=100)
    manuf = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    pdf = models.CharField(max_length=200)
    octo = models.CharField(max_length=200)
    search = models.CharField(max_length=100)
    search_enc = models.CharField(default="", max_length=100)
    time = models.DateTimeField(default=now, editable=False)

    img_big = models.CharField(max_length=200)
    img_big2 = models.CharField(max_length=200)
    img_big3 = models.CharField(max_length=200)
    img_big4 = models.CharField(max_length=200)
    img_small = models.CharField(max_length=200)
    img_footprint = models.CharField(max_length=200)
    img_symbol = models.CharField(max_length=200)

    farnell_mnu = models.CharField(max_length=50)
    farnell_czk = models.CharField(max_length=50)
    mouser_mnu = models.CharField(max_length=50)
    mouser_eur = models.CharField(max_length=50)
    digikey_mnu = models.CharField(max_length=50)
    digikey_usd = models.CharField(max_length=50)

    specs = JSONField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class HistoryPart(BasePart):
    pass

class FavouritePart(BasePart):
    pass