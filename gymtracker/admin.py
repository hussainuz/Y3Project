from django.contrib import admin

from .models import Profile, Following, Workout, Exercise, Set, Stored_Exercise

admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Set)
admin.site.register(Stored_Exercise)