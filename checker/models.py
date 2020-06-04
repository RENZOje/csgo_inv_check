from django.db import models

# Create your models here.


class Item(models.Model):

    name = models.CharField(max_length=300, null=True)
    link_img = models.CharField(max_length=500, null=True)
    link_inspect = models.CharField(max_length=500, null=True)
    float = models.FloatField(null=True)
    color = models.CharField(max_length=50, null=True)
    # trade_lock = models.CharField(max_length=100, null=True)
    amount = models.IntegerField(null=True)
    class_item = models.CharField(max_length=50, null=True)
    expiration_data = models.CharField(max_length=50, null=True)
    price_av_week = models.FloatField(null=True)
    condition = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name



class Query(models.Model):
    total_price = models.FloatField(null=True)
    time_q = models.DateTimeField(auto_now_add=True)
    items = models.TextField(null=True)

    def __str__(self):
        return self.time_q
