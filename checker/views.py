from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checker.executor import *
from django.views.generic import DetailView

from .forms import *
import ast
# Create your views here.

@login_required(login_url='login')
def create_new_query(requests):


    query_id = requests.GET.get('q', None)

    return _execute(requests, query_id)


@login_required(login_url='login')
def refresh_query(requests):

    query_id = requests.user.profile.steam_id64

    return _execute(requests, query_id)





def _execute(requests, query_id):
    instance_item = []
    if query_id:
        try:
            items = executor(query_id)
        except:
            context = {}
            messages.error(requests, 'Wrong Steam id64!')
            return render(requests, 'main.html', context=context)

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
                condition=items['condition'][i])

            instance_item.append(item)
            query_item_list.append(item.id)

        total_price = []
        for i in range(0, len(items['price'])):
            total_price.append(items['price'][i] * items['amount'][i])
        total_price = round(sum(total_price), 2)

        query = Query.objects.create(profile_create=int(query_id), items=query_item_list, total_price=total_price)

        print(requests.user.profile.steam_id64)
        print(query_id)

        if requests.user.profile.steam_id64 != query_id:
            print(requests.user.profile.steam_id64 != query_id)
            print(requests.user.profile.steam_id64)
            print(query_id)
            requests.user.profile.friend_search = ast.literal_eval(requests.user.profile.friend_search) + [query.id]
            requests.user.profile.save()

        context = {'items': instance_item, 'total_price': total_price}

        return render(requests, 'main.html', context=context)
    else:
        context = {}
        return render(requests, 'main.html', context=context)



@login_required(login_url='login')
def get_last_query(request):


    try:
        query = Query.objects.filter(profile_create=request.user.profile.steam_id64).latest()
        if query:
            instance_item = []
            items_id = ast.literal_eval(query.items)
            for item_id in items_id:
                item = Item.objects.get(id=item_id)
                instance_item.append(item)



            context = {'items': instance_item, 'total_price': query.total_price, 'time_creation': query.time_q}
            return render(request, 'main.html', context=context)
        else:
            context = {}
            return render(request, 'main.html', context=context)
    except:
        context = {}
        return render(request, 'main.html', context=context)


@login_required(login_url='login')
def get_detail_query(request, pk):

    try:
        query = Query.objects.get(id=pk)
        if query:
            instance_item = []
            items_id = ast.literal_eval(query.items)
            for item_id in items_id:
                item = Item.objects.get(id=item_id)
                instance_item.append(item)



            context = {'items': instance_item, 'total_price': query.total_price, 'time_creation': query.time_q}
            return render(request, 'main.html', context=context)
        else:
            context = {}
            return render(request, 'main.html', context=context)
    except:
        context = {}
        return render(request, 'main.html', context=context)






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
                user_ins = form.instance
                Profile.objects.create(user=user_ins)
                return redirect('login')

        context = {'form':form}

        return render(request,'registration.html',context=context)

@login_required(login_url='login')
def user_page(request):

    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()


    my_query = Query.objects.filter(profile_create=profile.steam_id64)


    friends_query = [Query.objects.get(id=x) for x in ast.literal_eval(profile.friend_search)]


    if my_query or friends_query:
        context = {'form': form, 'my_query': my_query , 'friends_query':friends_query}
        return render(request, 'profile.html', context=context)

    else:
        context = {'form': form}
        return render(request, 'profile.html', context=context)





@login_required(login_url='login')
def help(request):

    return render(request,'help.html')


