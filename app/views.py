from django.shortcuts import redirect, render
from datetime import datetime
from app.models import Contact,Cuser

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

def index(request):
    return render(request,"index.html")


def about(request):
    return render(request,"about.html")

def userlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            context = {"status":"User not found"}
            return render(request,"login.html",context) 
    else:
        return render(request,"login.html")


def regisiter(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        occupation = request.POST.get('occupation')
        salary = request.POST.get('salary')
        education = request.POST.get('education')
        profile = request.FILES.get('profile')
        city = request.POST.get('city')
        age = request.POST.get('age')
        state = request.POST.get('state')
        reigion = request.POST.get('reigion')
        mothertoug = request.POST.get('mothertoug')
        if cpassword != password:
            context = {"status":"Password is not equal to confirm password"}
            return render(request,"regisiter.html",context)
        mydata = Cuser.objects.filter(username=username).values() | Cuser.objects.filter(email=email).values() | Cuser.objects.filter(phone=phone).values()
        if mydata :
            context = {"status":"user already found"}
            return render(request,"regisiter.html",context)
        else:
            cuser = Cuser(name=name,username=username,email=email,phone=phone,gender=gender,password=password,occupation=occupation,salary=salary,education=education,city=city,age=age,state=state,reigion=reigion,image=profile,mothertoug=mothertoug)
            cuser.save()
            user = User.objects.create_user(username,email,password)
            user.save()
            login(request, user)
            return redirect(index)
    else:
        return render(request,"regisiter.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        query = request.POST.get('query')
        contact = Contact(name=name,email=email,phone=number,query=query,date=datetime.today())
        contact.save()
        context = {"submit":contact}
        return render(request,"contact.html",context)
    else:
        return render(request,"contact.html")


def profile(request):
    if request.user.is_authenticated:
        data = Cuser.objects.filter(username=request.user).values()
        context = {"data":data[0]}
        return render(request,"profile.html",context)
    else:
        return redirect(login)


def userlogout(request):
    logout(request)
    return redirect(index)


def editprofile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            education = request.POST.get('education')
            occupation = request.POST.get('occupation')
            reigion = request.POST.get('reigion')
            mothertoug = request.POST.get('mothertoug')
            city = request.POST.get('city')
            state = request.POST.get('state')
            cuser = Cuser.objects.get(username=request.user)
            cuser.name = name
            cuser.age = age
            cuser.email = email
            cuser.phone = phone
            cuser.education = education
            cuser.occupation = occupation
            cuser.reigion = reigion
            cuser.mothertoug = mothertoug
            cuser.city = city
            cuser.state = state
            cuser.save()
            return redirect(profile)


def findbest(request):
    if request.method == "POST":
        cuser = Cuser.objects.all().values()
        context = {"data":cuser}
        return render(request,"findbest.html",context)      
    return render(request,"findbest.html")   