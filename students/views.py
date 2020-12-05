from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from courses.models import Course
from .forms import CourseEnrollForm


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


def enroll_course(request,pk) :
    
        course = Course.objects.get(pk=pk)
        course.student_courses.add(request.user.student)
        chat = course.general_chat
        chat.participants.add(request.user)

        return redirect('students:student_course_detail',
                                pk=course.id)
    
    

    


class CourseListView(ListView):
    model = Course
    template_name = 'students/course/all_courses.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            return qs
        if self.request.user.role == 'S':
            return qs.exclude(student_courses__in=[self.request.user.student])
        else:
            return qs


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(student_courses__in=[self.request.user.student])


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(student_courses__in=[self.request.user.student])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                                    id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]

        context['announcements'] = self.object.announcements.all()
        
        return context
