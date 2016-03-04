from django.db import models

class Address(models.Model):
    '''
    Represents an address entered in the system.
    '''
    # duplicates aren't allowed on Fusion, so for sanity, we don't want them here either.
    desc = models.CharField(max_length=255, null=False, blank=False, unique=True)
    lng = models.FloatField(null=False, blank=False)
    lat = models.FloatField(null=False, blank=False)
    
