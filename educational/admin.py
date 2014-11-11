from django.contrib import admin
from .models import Discipline, Assignment, Deadline
# Register your models here.
admin.site.register(Discipline)
admin.site.register(Assignment)
admin.site.register(Deadline)
