from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.contrib.auth import login,logout,authenticate
from . models import StudentModel
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# Create your views here.
def index(request):
    return render(request,'index/index.html')
def calculate(request):
    if request.method=="POST":
        gend=request.POST.get("gend")
        if gend=="Male":
            gend=1
        else:
            gend=0
        height=int(request.POST.get("height"))
        print(gend,height)
        df=pd.read_csv('index/weight-height.csv')
        df['Gender']=pd.get_dummies(df['Gender'],drop_first=True)
        std_val=df['Height'].std()
        meanval=df['Height'].mean()
        std_3=meanval+2.5*std_val
        n_std_3=meanval-2.5*std_val
        newdf=df[(df['Height']>=n_std_3)&(df['Height']<=std_3)]
        x=newdf.drop(['Weight'],axis=1)
        y=newdf['Weight']
        xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=12)
        LR=LinearRegression()
        LR.fit(xtrain,ytrain)
        result=round(float(LR.predict([[gend,height]]))/2.2046)
        if gend==1:
            gend="Male"
        else:
            gend="Female"
        return render(request,'index/calculate.html',{
            'result':result,
            'gend':gend,
            'height':np.round(height)
        })
    return render(request,'index/calculate.html')
def calculation(request):
    if request.method=="POST":
        gend=request.POST.get("gend")
        if gend=="Male":
            gend=1
        else:
            gend=0
        height=int(request.POST.get("height"))
        print(gend,height)
        df=pd.read_csv('index/weight-height.csv')
        df['Gender']=pd.get_dummies(df['Gender'],drop_first=True)
        std_val=df['Height'].std()
        meanval=df['Height'].mean()
        std_3=meanval+2.5*std_val
        n_std_3=meanval-2.5*std_val
        newdf=df[(df['Height']>=n_std_3)&(df['Height']<=std_3)]
        x=newdf.drop(['Weight'],axis=1)
        y=newdf['Weight']
        xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=12)
        LR=LinearRegression()
        LR.fit(xtrain,ytrain)
        result=round(float(LR.predict([[gend,height]]))/2.2046)
        if gend==1:
            gend="Male"
        else:
            gend="Female"
        StudentModel.objects.create(
            user=request.user,
            Gender=gend,
            Height=height,
            Weight=result
        )
        return render(request,'index/calculation.html',{
            'result':result,
            'gend':gend,
            'height':np.round(height)
        })
    if not request.user.is_authenticated:     
        user=User.objects.all().last()
        name=f"user-{user.id+1}"
        usr=User.objects.create(
            username=name
        )
        login(request,usr);
        return redirect('calculation')
    return render(request,'index/calculation.html')
def user_logout(request):
    logout(request)
    return redirect('/')
def user_login(request):
    if request.method=="POST":
        username=str(request.POST.get('userid').lower())
        try:
            usr=User.objects.get(username=username)
            login(request,usr)
            return redirect('calculation')
        except Exception:
            pass
        return redirect('calculation')
    return render(request,'index/user_login.html')
def all_result(request):
    datas=StudentModel.objects.filter(user=request.user).order_by('-date')
    return render(request,'index/all_result.html',{
        'datas':datas
    })