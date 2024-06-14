from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
import numpy as np
from .models import pics
from PIL import Image
from tensorflow.keras.models import load_model
import os
import cv2

import os
import shutil
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def home(request):
    return render(request, "index.html")

def diagnosis(requests):
    if requests.method=='GET':
        params={'disp':False}
        return render(requests,'diagnosis.html',params)
    else:
        # img=requests.FILES['img']
        # obj=pics.objects.create(img=img)
        # image=Image.open(obj.img)
        # image=np.array(image)
        # image=cv2.resize(image,(100,100))/255
        # image=np.expand_dims(image,axis=0)
        # ---resized_image = cv2.resize(image, (100, 100))
        # ---image = np.expand_dims(resized_image, axis=0)

        img = requests.FILES['img']
        shutil.rmtree(os.getcwd()+'\\media')
        path1 = default_storage.save(os.getcwd()+'\\media\\result.jpg', img)
        tmp_file = os.path.join(settings.MEDIA_ROOT, path1)

        # img = Image.open(tmp_file)
        img = cv2.imread(tmp_file)
        resized_image = cv2.resize(img, (100, 100))
        image = np.expand_dims(resized_image, axis=0)


        base=os.getcwd()
        path=os.path.join(os.path.join(base,'home'),'static_home')
        path=os.path.join(path,'model.h5')
        model=load_model(path)
        y_pred_prob = np.around(model.predict(image), 3)
        max = np.max(y_pred_prob)
        pred=np.argmax(y_pred_prob)
        # print(y_pred_prob)
        label = {
            0:'Melanocytic nevi',
            1:'Melanoma',
            2:'Benign keratosis-like lesions',
            3:'Basal cell carcinoma',
            4:'Actinic keratoses',
            5:'Vascular lesions',
            6:'Dermatofibroma'
        }
        
        if max > 0.65 :
            params={'disease':label[pred],'disp':True,'val':pred,'max':round(max*100,2)}
        else:
            params={'disease':'No Disease Found','disp':True,'val':7,'max':None}
        
        

        # Compute predictions
        # y_pred_prob = np.around(model.predict(image), 3)
        # y_pred = np.argmax(y_pred_prob, axis=1)
        # print(y_pred_prob)
        return render(requests,'diagnosis.html',params)


def signup(requests):
    if requests.method=='GET':
        return render(requests,'signup.html')
    else:
        name=requests.POST['name']
        username=requests.POST['username']
        password=requests.POST['pass']
        cpassword = requests.POST['cpass']
        age=requests.POST['age']
        blood=requests.POST['blood']
        email=requests.POST['email']

        bg=['O+','O-','B+','B-','A+','A-','AB+','AB-']

        if blood not in bg:
            messages.info(requests, 'Enter a valid blood group')
            return redirect('signup')

        if age.isdigit()==False:
            messages.info(requests, 'Age should be a digit')
            return redirect('signup')

        if name.isalpha()==False:
            messages.info(requests,'Name should contain only alphabets')
            return redirect('signup')
        if(password!=cpassword):
            messages.info(requests,'Both the passwords should match')
            return redirect('signup')
        if(User.objects.filter(username=username).exists()):
            messages.info(requests, 'Username already exists')
            return redirect('signup')

        user=User.objects.create_user(username=username,email=email,password=password,first_name=name)
        user.save()
        user1=auth.authenticate(username=username,password=password)
        if user1 is not None:
            auth.login(requests,user1)
        return redirect('/')


def login(requests):
    if requests.method == 'GET':
        return render(requests, 'login.html')
    else:
        username=requests.POST['uname']
        password=requests.POST['pass']
        user1 = auth.authenticate(username=username, password=password)
        if user1 is not None:
            auth.login(requests, user1)
            return redirect('/')
        else:
            messages.info(requests,'Invalid credentials')
            return redirect('login')

def logout(requests):
    auth.logout(requests)
    return redirect('/')


def logout(requests):
    auth.logout(requests)
    return redirect('/')

def about(request):
    return render(request, "about.html")

def workflow(request):
    return render(request, "workflow.html")

def skindisorders(request):
    return render(request, "skindisorders.html")

# def diagnosis(request):
#     return render(request, "diagnosis.html")
