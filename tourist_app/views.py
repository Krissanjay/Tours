from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.permissions import AllowAny

from tourist_app.forms import TourForm
from tourist_app.models import Tour
from tourist_app.serializers import TourSerializers

import requests
# Create your views here.


class TourCreateView(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializers
    permission_classes = [AllowAny]

class TourUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializers

class TourDetailView(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializers

class TourDelete(generics.DestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializers

class TourSearch(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializers

    def get_queryset(self):
        name=self.kwargs.get('name')
        return Tour.objects.filter(name__icontains=name)


def create(request):
    if request.method=='POST':
        form=TourForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                form.save()
                api_url='http://127.0.0.1:8000/create/'
                data=form.cleaned_data

                response=requests.post(api_url,data=data,files={'image1':request.FILES['image1'],'image2':request.FILES['image2']})

                if response.status_code == 400:
                    messages.success(request,'Tour created Successfully!')
                    return redirect('/')
                else:
                    messages.error(request,"Error!")
            except requests.RequestException as e:
                messages.error(request,f'Error during api request{str(e)}')
        else:
            messages.error(request,"Form is invalid!")

    else:
        form=TourForm()

    return render(request,'create.html',{'form':form})

def details(request,id):
    api_url=f'http://127.0.0.1:8000/detail/{id}'
    response=requests.get(api_url)
    if response.status_code==200:
        data=response.json()
        description=data['description'].split(',')
        return render(request,'details.html',{'data':data,'description':description})
    return render(request,'details.html')

def update(request,id):
    if request.method=='POST':
        name=request.POST['name']
        weather=request.POST['weather']
        state=request.POST['state']
        district=request.POST['district']
        link=request.POST['link']
        description=request.POST['description']
        api_url=f'http://127.0.0.1:8000/update/{id}/'
        data={
            'name':name,
            'weather':weather,
            'state':state,
            'district':district,
            'link':link ,
            'description':description
        }
        files={'image1':request.FILES.get('image1'),'image2':request.FILES.get('image2')}
        response=requests.put(api_url,data=data,files=files)
        if response.status_code==200:
            messages.success(request,'Updated successfully')
            return redirect('/')
        else:
            messages.error(request,f'Error submitting data to the Rest api :{response.status_code}')
    api_url=f'http://127.0.0.1:8000/detail/{id}/'
    response=requests.get(api_url)
    data=response.json()
    return render(request,'update.html',{'data':data})

def index(request):
    if request.method=='POST':
        search=request.POST['search']
        api_url=f'http://127.0.0.1:8000/search/{search}/'

        try:
            response=requests.get(api_url)
            if response.status_code==200:
                data=response.json()
            else:
                data=None
        except requests.RequestException as e:
            data=None
        return render(request,'index.html',{'data':data})
    else:
        api_url='http://127.0.0.1:8000/create/'
        try:
            response=requests.get(api_url)
            if response.status_code==200:
                data=response.json()

                paginator=Paginator(data,3)
                page_number=request.GET.get('page')
                original_data=paginator.get_page(page_number)
                return render(request,'index.html',{'original_data':original_data})
            else:
                return render(request,'index.html',{'error message':f'Error:{response.status_code}'})
        except requests.RequestException as e:
            return render(request,'index.html',{'error_message':f'Error:{str(e)}'})


def delete(request,id):
    api_url=f'http://127.0.0.1:8000/delete/{id}/'
    print(id)
    response=requests.delete(api_url)
    if response.status_code==200:
        print(f'item with {id} has been deleted')
        messages.info(request,f'item with {id} has been deleted')
        return redirect('/')
    else:
        print(f'Failed to delete item status code {response.status_code}')
    return redirect('/')

def tr(request):
    return render(request,'index.html')