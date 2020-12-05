from django.shortcuts import render
from .models import *
from courses.models import Announcement,Course
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from courses.models import Course
from accounts.models import Student
from datetime import datetime
# Create your views here.

@login_required(login_url = '/accounts/login/')
def parent_index(request) :
    
    user = request.user

    if user.role !="P" :
        return redirect('accounts:logout')

    courses =  Course.objects.filter(student_courses__in= user.parent.children.all()).all()
    announcements = Announcement.objects.filter(course__in =courses).all()

    holidays = Holidays.objects.filter(date__gte = datetime.now()).all()
    events = Events.objects.filter(date__gte = datetime.now()).all()
    context ={
        'announcements' : announcements,
        'holidays': holidays,
        'events' : Events.objects.filter(date__gte = datetime.now()).all(),
        'childs' : user.parent.children.all(),
    }

    return render(request,'parent/parent.html',context)



def grade_card(request, pk) :
    student = Student.objects.get(pk=pk)
    reports = student.reports.all()
    
    return render(request,'parent/report.html',{'reports':reports,'student':student})




