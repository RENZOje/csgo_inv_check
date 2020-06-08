from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True,default='profile_def.png')
    steam_id64 = models.CharField(max_length=17, null=True, default='')

    def __str__(self):
        return f'{self.user.username} {self.steam_id64}'


class Query(models.Model):
    profile_create = models.CharField(max_length=17, null=True, default='')
    total_price = models.FloatField(null=True)
    time_q = models.DateTimeField(auto_now_add=True, null=True)
    items = models.TextField(null=True)


    def __str__(self):
        return str(self.time_q)


    class Meta:
        get_latest_by = 'time_q'

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