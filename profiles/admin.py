from django.contrib import admin

from profiles.models import Profile, Student, Teacher, Guardian, Group

admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Guardian)
admin.site.register(Group)

