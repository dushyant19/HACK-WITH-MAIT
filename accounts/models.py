from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
#from django.http import HttpResponseBadRequest
from django.db.models.signals import post_save
    

# Create your models here.
from django.conf import settings 
FEES = [1000*i for i in range(1,13)]

class User(AbstractUser) :
    class Role(models.TextChoices) :
        STUDENT = "S" ,_("Student")
        PARENT = "P" ,_("Parent")
        TEACHER = "T",_("Teacher")
    role = models.CharField(max_length = 255,choices=Role.choices)
    is_approved= models.BooleanField(default=False)

class Teacher(models.Model) :
    user = models.OneToOneField(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE, related_name="teacher")
    position = models.CharField(max_length=255,blank=True)
    department = models.CharField(max_length=255,blank=True)
    date_of_joining = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.username

class Parent(models.Model) :
    user = models.OneToOneField(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)
    @property
    def total_fees_to_be_paid(self) :
        for child in self.children.all():
            fees+= child.fess
        return fees

    def __str__(self):
        return self.user.username
        


class Student(models.Model) :
    user = models.OneToOneField(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE, related_name="student")
    roll_no = models.IntegerField(null=True)
    parent = models.ForeignKey(Parent,related_name="children",null=True,on_delete=models.CASCADE)
    standard = models.IntegerField(default =1)
    is_fees_paid = models.BooleanField(default = False)
    date_of_joining = models.DateField(default =timezone.now)
    courses = models.ManyToManyField('courses.Course',related_name="student_courses",through="StudentToCourses", null=True)

    @property
    def fees(self) :
        return  0 if self.fess_is_paid else Fess[self.standard]
    
    def __str__(self):
        return self.user.username



class StudentToCourses(models.Model) :
    class Grade(models.TextChoices) :
        A = "A" ,_("A")
        B = "B" ,_("B")
        C = "C",_("C")
        D = "D",_("D")
        E = "E",_("E")
    grade = models.CharField(max_length = 255,choices=Grade.choices, null=True, blank=True)
    attendance = models.IntegerField(null=True)
    student = models.ForeignKey(Student,related_name="reports",null=True,on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course',related_name="report_cards",null=True,on_delete=models.CASCADE)
    




@receiver(post_save,sender= User) 
def generate_profile(sender,instance,created,**kwargs) :
    role = instance.role 
    print(role)
    
    if created :
        if role=="S" :
                Student.objects.create(user=instance) 
        elif role=="T" :
                Teacher.objects.create(user=instance)
        elif role=="P" :
                Parent.objects.create(user=instance)
    




