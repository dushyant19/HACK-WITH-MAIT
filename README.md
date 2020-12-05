# Hackccelerate

An Online education platfrom for schools 
Live at https://learn-live.herokuapp.com/

## Test User Credentials

Login -> http://learn-live.herokuapp.com/accounts/login/

### Student Login
Username : student01
Password : common101

### Teacher Login
Username : teacher01
Password : common101

### Parent Login
Username : parent01
Password : common101

### Django SuperUser
login -> http://learn-live.herokuapp.com/admin
Username : ayush
Password : a

## Installation
```bat
git clone 
cd 
pip install -r 'requirements.txt'
python manage.py makemigrations
python manage.py migrate

```

- Cache db settings
- memached for cache
In settings.py change the "CHANNEL_LAYERS" configuration to your local redis server

```bat
python manage.py runserver
```

Note 01: Once user register on portal, admin should login <here>[https://learn-live.herokuapp.com/admin/accounts/user/] and approve the account of that user. Only approved users can view our course content and participate in discussion forum.

Note 02: All the Test Credentials are approved Users. So you can use them freely!

## Features 

### Students

- login and register
- enroll to available courses
- see all courses 
- navigation to course where they can see different modules, contents of modules, announcments regarding the course.
- Chat with other students enrolled in that course through course chat room
- Participate in dicussion forum with other teachers/parents/students


### Teachers
- Login and register
- Create multiple courses
- Edit/create new modules in each course
- Reorder modules whenever you feel necessary!
- Post course content in any way. It can be text/image/video/audio/ppt/pdf/etc... 
- Participate in dicussion forum with other teachers/parents/students
- Create Announcements in each course separately (Course Specific)


### Parents
- Login and register
- See announcements regarding their children's courses that are made by teachers
- Get list of all Events 
- Get list of all Holiays
- Check progress of each student in every course (grades,attendance) 
- Participate in dicussion forum with other teachers/parents/students

Note : Attendance and grades need to be registered by the admin once finalised.


## Technology Used
- Django 
- Django Rest Framework
- Django Channels
- Tailblocks
- Javascript
- JQuery
- Html
- CSS

We tried to follow the best coding principles while participating in this hackathon!

