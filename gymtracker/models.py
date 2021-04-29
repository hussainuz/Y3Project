from django.db import models
from django.contrib.auth.models import User


class Profile(User):
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)

    def get_connections(self):
        following = Following.objects.filter(current_user=self.user)
        return following

    def __str__(self):
        return self.username

class Following(models.Model):
    current_user = models.ForeignKey(Profile, related_name="user", on_delete=models.CASCADE)
    following_user = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} follows {}'.format(self.current_user, self.following_user)

class Workout(models.Model):
    owner = models.ForeignKey(Profile, related_name="workout_owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    datetime_added = models.DateTimeField(auto_now_add=True)#sort out format

    def __str__(self):
        return '{} : {} on {}'.format(self.owner, self.name,self.datetime_added)

class Exercise(models.Model):
    workout = models.ForeignKey(Workout, related_name="workout", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    #num_of_sets = models.IntegerField(default=0)

    def getSets(self):
        sets = Set.objects.filter(exercise=self).count()
        return sets

    def __str__(self):
        return self.name

class Set(models.Model):
    exercise = models.ForeignKey(Exercise, related_name="exercise", on_delete=models.CASCADE)
    set_no = models.IntegerField(null=True)
    reps = models.IntegerField(default=1)
    weight = models.DecimalField(default=0,max_digits=6,decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return '{} set {}'.format(self.exercise, self.set_no)


class Stored_Exercise(models.Model):
    name = models.CharField(max_length=50)
    link = models.URLField(max_length=200)

    def __str__(self):
        return self.name











