from django.shortcuts import render
from checker.executor import *
from .models import Item, Query

# name = models.CharField(max_length=300, null=True)
# link_img = models.CharField(max_length=500, null=True)
# link_inspect = models.CharField(max_length=500, null=True)
# float = models.FloatField(null=True)
# color = models.CharField(max_length=50, null=True)
# # trade_lock = models.CharField(max_length=100, null=True)
# amount = models.IntegerField(null=True)
# class_item = models.CharField(max_length=50, null=True)
# expiration_data = models.CharField(max_length=50, null=True)
# price_av_week = models.IntegerField(null=True)
# condition = models.CharField(max_length=50, null=True)




# Create your views here.
def view_main(requests):
    instance_item = []
    query_id = requests.GET.get('q', None)
    if query_id:
        items = executor(query_id)

        query_item_list = []
        for i in range(len(items['rd_full_name'])):
            item = Item.objects.create(
                name=items['rd_full_name'][i],
                link_img=items['rd_icon_url'][i],
                link_inspect=items['rd_inspect_url'][i],
                float=items['float'][i],
                color=items['color'][i],
                amount=items['amount'][i],
                class_item=items['class_item'][i],
                expiration_data=items['expiration'][i],
                price_av_week=items['price'][i],
                condition=items['condition'][i]  )

            instance_item.append(item)
            query_item_list.append(item.id)

        total_price = sum(items['price'])

        query = Query.objects.create(items=query_item_list, total_price=total_price)

        context = {'items':instance_item, 'total_price':total_price}

        return render(requests, 'main.html',context=context)
    else:
        context = {}
        return render(requests, 'main.html',context=context)

