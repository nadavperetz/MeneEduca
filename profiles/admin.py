from django.contrib import admin

from profiles.models import Profile, Student, Teacher, Guardian

admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Guardian)

