from django.shortcuts import render,redirect
from accounts.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponse
from accounts.models import *
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser

# Create your views here.



def user_login(request) :
    if request.method == "POST" :    
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password=password)

        if user is not None and user.is_approved :  
            login(request,user)       
            role = user.role 
            
            if role =="S" :
                return redirect('students:student_course_list')
            elif role=="T" :
                return redirect('courses:manage_course_list')
            elif role =="P" :
                return redirect('parents:parent_index') 
            else :
                messages.error(request,"Invalid credentials")
                return render(request,"accounts/login.html")        
        elif user is not None and not user.is_approved:
             login(request,user)  
             messages.info(request,"Approval needed")
             return redirect('accounts:approve')
        else :
             messages.error(request,"Invalid credentials")
             return render(request,"accounts/login.html")


    else :
        if request.user and not isinstance(request.user ,AnonymousUser) and request.user.is_approved:
            role = request.user.role 
            if role =="S" :
                return redirect('students:student_course_list')
            elif role=="T" :
                return redirect('courses:manage_course_list')
            elif role =="P" :
                return redirect('') 
            else :
                messages.error(request,"Invalid credentials")
                return render(request,"accounts/login.html")
        elif request.user and not isinstance(request.user ,AnonymousUser) and not request.user.is_approved:
             login(request,request.user)  
             messages.info(request,"Approval needed")
             return redirect('accounts:approve')
           
        else :
          return render(request,"accounts/login.html")


class Logout(LoginRequiredMixin,View):

    def get(self,request):
        logout(request)
        return redirect('accounts:login')

logout_user = Logout.as_view()


def approve(request) :
    return render(request,'accounts/approve.html')



def register_student(request) :
    if request.method =="POST" :
        first_name =request.POST["first_name"]
        last_name = request.POST["last_name"]
        roll_no = request.POST["roll_no"]
        password = request.POST["password"]
        email=request.POST["password"]
        standard = request.POST["standard"]
        password_cnf = request.POST["confirm_password"]
        username =first_name +str(roll_no)+str(standard)

        if User.objects.filter(username = username).exists() :
            username = username+"_"+str(len(User.objects.filter(username = username))+1)

        if password != password_cnf :
            messages.error(request,"Password Don't match")
            return render(request,"accounts/signup/teacher.html")

        user = User.objects.create(first_name=first_name,last_name=last_name,password=password,email=email,role="S",username=username)
        user.set_password(password)
        user.save() 

        user.student.roll_no = roll_no
        user.student.standard= standard
        user.student.save()

        return redirect("accounts:login")

    else :
        return render(request,'accounts/signup/student.html')



def register(request) :
    return render(request,'accounts/signup.html')


def register_teacher(request) :
    if request.method =="POST" :
        first_name =request.POST["first_name"]
        last_name = request.POST["last_name"]
        department = request.POST["department"]
        password = request.POST["password"]
        password_cnf = request.POST["confirm_password"]
        email=request.POST["email"]
        username =first_name +last_name+department

        if password != password_cnf :
            messages.error(request,"Password Don't match")
            return render(request,"accounts/signup/teacher.html")

        if User.objects.filter(username = username).exists() :
            username = username+"_"+str(len(User.objects.filter(username = username))+1)
        user = User.objects.create(first_name=first_name,last_name=last_name,password=password,email=email,role="T",username=username)
        user.set_password(password)
        user.save()

        user.teacher.department =department
        
        user.teacher.save()

        return redirect("accounts:login")

    else :
        return render(request,'accounts/signup/teacher.html')


def register_parent(request) :
    if request.method =="POST" :
        first_name =request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        email=request.POST["email"]
        parent_of =request.POST["parent_of"]
        password_cnf = request.POST["confirm_password"]
        username =first_name+last_name

        if User.objects.filter(username = username).exists() :
            username = username+"_"+str(len(User.objects.filter(username = username))+1)

        if password != password_cnf :
            messages.error(request,"Password Don't match")
            return render(request,"accounts/signup/teacher.html")

        user = User.objects.create(first_name=first_name,last_name=last_name,email=email,role="P",username=username)
        user.set_password(password)
        user.save() 
        child_list = list(parent_of.split(','))
        for c in child_list :
             user.parent.children.add(User.objects.get(username=c).student)

        return redirect("accounts:login")

    else :
        return render(request,'accounts/signup/parent.html')



