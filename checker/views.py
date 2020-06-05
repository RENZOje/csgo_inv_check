from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checker.executor import *
from .models import Item, Query
from .forms import CreateUserForm

# Create your views here.

@login_required(login_url='login')
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

        total_price = round(sum(items['price']),2)

        query = Query.objects.create(items=query_item_list, total_price=total_price)

        context = {'items':instance_item, 'total_price':total_price}

        return render(requests, 'main.html',context=context)
    else:
        context = {}
        return render(requests, 'main.html',context=context)



def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home_page')
            else:
                messages.info(request,'Username or password is incorrect')


        context = {}
        return render(request,'login.html',context=context)

def logout_page(request):
    logout(request)

    return redirect('login')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,f'Account created for {user}')

                return redirect('login')

        context = {'form':form}

        return render(request,'registration.html',context=context)
