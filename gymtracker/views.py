from django.shortcuts import render,redirect

from django.http import HttpResponse, Http404
from django.db import IntegrityError

from .models import User, Profile, Following, Workout, Exercise, Set, Stored_Exercise

appname = 'GymTracker'

def index(request):
    context = {'appname': appname}
    return render(request, 'gymtracker/index.html', context)

def signup(request):

    context = {'appname': appname}
    return render(request, 'gymtracker/signup.html', context)

def signup_processing(request):

    if 'username' in request.POST and 'email' in request.POST and 'fname' in request.POST and 'lname' in request.POST  and 'dob' in request.POST and 'password' in request.POST:
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        dob = request.POST["dob"]
        password = request.POST["password"]

    profile = Profile(username = username, email = email, first_name = fname, last_name = lname, date_of_birth = dob)
    profile.set_password(password)

    try: profile.save()
    except IntegrityError: raise Http404('This username or password is already taken')
    context = {'appname': appname,'logIn':True}
    return render(request, 'gymtracker/home.html', context)

def signin(request):
    context = {'appname': appname}
    return render(request, 'gymtracker/signin.html', context)

def signin_processing(request):

    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST["username"]
        password = request.POST["password"]

        try: profile = Profile.objects.get(username = username)
        except Profile.DoesNotExist :
            
            context = {'appname': appname, 'error': 'Please Enter the Correct LoginIn Details'}
            return render(request, 'gymtracker/signin.html', context)

        if profile.check_password(password):

            #Set session variables for the user logged in
            request.session['username'] = username

            context = {'logIn': True, 'name': username, 'appname': appname}
            return render(request, 'gymtracker/home.html', context)
        else:
            #raise Http404('Incorrect Password')
            context = {'appname': appname, 'error': 'Please Enter the Correct Login In Details'}
            return render(request, 'gymtracker/signin.html', context)

def verify_loggedin(view):
    def usercheck(request):
        if 'username' in request.session:
            username = request.session['username']
            try: profile = Profile.objects.get(username=username)
            except Profile.DoesNotExist : raise Http404("User does not exist")
            return view(request, profile)
        else:
            context = {'appname': appname}
            return render(request, 'gymtracker/signin.html', context)
    return usercheck

@verify_loggedin
def home(request,profile):
    context = {'appname': appname, 'logIn': True,}
    return render(request, 'gymtracker/home.html', context)

@verify_loggedin
def signout(request, profile):
    request.session.flush()
    context = {'appname': appname}
    return render(request, 'gymtracker/signout.html', context)

@verify_loggedin
def friends(request, profile):
    followings=Following.objects.all().filter(current_user = profile)
    context = {'appname': appname, 'logIn': True, 'followings':followings }
    return render(request, 'gymtracker/friends.html', context)

@verify_loggedin
def search_friend(request, profile):
    context = {'appname': appname}
    context.update({'profile': profile, 'logIn': True})
    return render(request, 'gymtracker/search_friend.html', context)


@verify_loggedin
def display_searched_user(request,profile):
    context = {'appname': appname}
    if 'username' in request.POST:
        searched_user = request.POST["username"]
        if Profile.objects.filter(username = searched_user).exists():
            friend = Profile.objects.get(username = searched_user)
            isFollowing = checkFollowing(profile,friend)
            context.update({'profile': profile, 'logIn': True, 'friend': friend, 'isFollowing':isFollowing})
            return render(request, 'gymtracker/display_searched_user.html', context)
        else:
            friend = None
            context.update({'profile': profile, 'logIn': True, 'friend': friend, 'isFollowing':False})
            return render(request, 'gymtracker/display_searched_user.html', context)
        
def checkFollowing(profile,friend):
    followings = Following.objects.filter(current_user=profile)
    for x in followings:
        if x.following_user == friend:
            return True
    return False


@verify_loggedin
def add_friend(request, profile):
    context = {'appname': appname}
    if 'fpk' in request.POST:
        current_user = Profile.objects.get(pk = profile)
        searched_user_pk = request.POST["fpk"]
        friend = Profile.objects.get(pk = searched_user_pk)
        if(Following.objects.filter(current_user=current_user).filter(following_user=friend).exists()):
            pass
        else:
            Following.objects.create(current_user=current_user, following_user=friend)
        context.update({'profile': profile, 'logIn': True, 'friend': friend})
        return render(request, 'gymtracker/add_friend.html', context)

@verify_loggedin
def remove_friend(request, profile):
    context = {'appname': appname}
    if 'fpk' in request.POST:
        current_user = Profile.objects.get(pk = profile)
        searched_user_pk = request.POST["fpk"]
        friend = Profile.objects.get(pk = searched_user_pk)
        
        if(Following.objects.filter(current_user=current_user).filter(following_user=friend).exists()):
            relationship = Following.objects.filter(current_user=current_user).filter(following_user=friend)
            relationship.delete()
        context.update({'profile': profile, 'logIn': True, 'friend': friend,'status':"Unfollowed"})
        return render(request, 'gymtracker/add_friend.html', context)

@verify_loggedin
def show_all_followings(request,profile):
    context = {'appname': appname,'logIn':True}
    followings = Following.objects.filter(current_user=profile)
    following_profiles = set()
    for x in followings:
        friend = Profile.objects.get(pk = x.following_user)
        following_profiles.add(friend)
    context.update({'followings':following_profiles})
    return render(request, 'gymtracker/show_all_followings.html', context)

@verify_loggedin
def following_record(request,profile):
    context = {'appname': appname, 'logIn':True}
    if 'fpk' in request.POST:
        selected_following_id = request.POST["fpk"]
        selected_following = Profile.objects.get(pk = selected_following_id)
        fworkouts = Workout.objects.filter(owner = selected_following).order_by('-datetime_added')
        context.update({'fworkouts':fworkouts})
    return render(request, 'gymtracker/following_record.html', context)

@verify_loggedin
def view_following_workout(request,profile):
    context = {'appname': appname, 'logIn':True}
    if 'wpk' in request.POST:
        fworkout_id = request.POST["wpk"]
        fworkout = Workout.objects.get(pk = fworkout_id)
        exercises = Exercise.objects.filter(workout = fworkout).order_by('-created_at')
        context.update({'fexercises':exercises,'fworkout':fworkout})
    return render(request, 'gymtracker/view_following_workout.html', context)

@verify_loggedin
def view_following_exercise(request,profile):
    context = {'appname': appname, 'logIn':True}
    if 'epk' in request.POST:
        fexercise_id = request.POST["epk"]
        fexercise = Exercise.objects.get(pk = fexercise_id)
        fsets = Set.objects.filter(exercise = fexercise)
        context.update({'fsets':fsets,'fexercise':fexercise})
    return render(request, 'gymtracker/view_following_exercise.html', context)


@verify_loggedin
def remove_friend_2(request, profile):
    context = {'appname': appname}
    if 'fpk' in request.POST:
        current_user = Profile.objects.get(pk = profile)
        searched_user_pk = request.POST["fpk"]
        friend = Profile.objects.get(pk = searched_user_pk)
        
        if(Following.objects.filter(current_user=current_user).filter(following_user=friend).exists()):
            relationship = Following.objects.filter(current_user=current_user).filter(following_user=friend)
            relationship.delete()
        context.update({'profile': profile, 'logIn': True, 'friend': friend})
        return redirect(show_all_followings)


@verify_loggedin
def add_workout(request,profile):
    context = {'appname': appname, 'logIn':True}
    return render(request, 'gymtracker/add_workout.html', context)

@verify_loggedin
def add_workout_processing(request,profile):
    context = {'appname': appname, 'logIn': True,}

    if 'workout_name' in request.POST:
        workout_name = request.POST["workout_name"]
        workout = Workout.objects.create(owner=profile,name=workout_name)
        
    if 'save' in request.POST: # continue and return to index
        return render(request, 'gymtracker/home.html', context)
        
    if 'continue' in request.POST: #move on to adding exercise
        exercises = Stored_Exercise.objects.all().order_by('name')
        context.update({'workout':workout,'exercises':exercises})
        return render(request, 'gymtracker/add_exercise.html', context)

@verify_loggedin
def add_exercise(request,profile):
    context = {'appname': appname, 'logIn':True}
    return render(request, 'gymtracker/add_exercise.html', context)

@verify_loggedin
def add_exercise_processing(request,profile):
    context = {'appname': appname, 'logIn': True,}

    if 'exercise_name' in request.POST:
        workout_name = request.POST["exercise_name"]
        workout_id = request.POST["wpk"]
        workout = Workout.objects.get(pk = workout_id)
        exercise = Exercise.objects.create(workout=workout,name=workout_name)

    if 'save' in request.POST: # continue and return to index
        return render(request, 'gymtracker/home.html', context)
        
    if 'continue' in request.POST: #move on to adding workout
        context.update({'exercise':exercise})
        return render(request, 'gymtracker/add_set.html', context)

@verify_loggedin
def add_set(request,profile):
    context = {'appname': appname, 'logIn':True}
    return render(request, 'gymtracker/add_exercise.html', context)

@verify_loggedin
def add_set_processing(request,profile):
    context = {'appname': appname, 'logIn': True,}

    if 'set' in request.POST:
        set_no = request.POST["set"]
        reps = request.POST["reps"]
        weight = request.POST["weight"]
        exercise_id = request.POST["epk"]
        exercise = Exercise.objects.get(pk = exercise_id)
        Set.objects.create(exercise=exercise,set_no=set_no,reps=reps,weight=weight)

    if 'save' in request.POST: # continue and return to index
        return render(request, 'gymtracker/home.html', context)
        
    if 'continue' in request.POST: #move on to adding workout
        context.update({'exercise':exercise})
        return render(request, 'gymtracker/add_set.html', context)

@verify_loggedin
def record(request,profile):
    context = {'appname': appname, 'logIn': True,}
    workouts = Workout.objects.filter(owner=profile).order_by('-datetime_added')

    context.update({'user':profile,'workouts':workouts})
    return render(request, 'gymtracker/record.html', context)

@verify_loggedin
def edit_workout(request,profile):
    context = {'appname': appname, 'logIn': True,}
    if 'wpk' in request.POST:
        workout_id = request.POST["wpk"]
        workout = Workout.objects.get(pk = workout_id)
        context.update({'workout':workout})

    return render(request,'gymtracker/edit_workout.html',context)

@verify_loggedin
def edit_workout_processing(request,profile):
    if 'workout' in request.POST:
        wname = request.POST["workout"]
        workout_id = request.POST["wpk"]
        workout = Workout.objects.get(pk = workout_id)
        workout.name = wname
        workout.save()
        return redirect(record)

@verify_loggedin
def add_exercise_later(request,profile):
    context = {'appname': appname, 'logIn': True,}
    if 'wpk' in request.POST:
        workout_id = request.POST["wpk"]
        workout = Workout.objects.get(pk = workout_id)
        exercises = Stored_Exercise.objects.all().order_by('name')
        context.update({'workout':workout,'exercises':exercises})

        return render(request,'gymtracker/add_exercise.html',context)


@verify_loggedin
def delete_workout(request,profile):
    if 'wpk' in request.POST:
        workout_id = request.POST["wpk"]
        workout = Workout.objects.get(pk = workout_id)
        workout.delete()

    return redirect(record)




@verify_loggedin
def view_workout(request,profile):
    context = {'appname': appname, 'logIn': True,}
    if 'wpk' in request.POST:
        workout_id = request.POST["wpk"]
        workout = Workout.objects.get(pk = workout_id)
        exercises = Exercise.objects.filter(workout=workout).order_by('-created_at')
        context.update({'exercises':exercises, 'workout':workout})

    return render(request,'gymtracker/view_workout.html', context)
    

@verify_loggedin
def edit_exercise(request,profile):
    context = {'appname': appname, 'logIn': True,}
    if 'epk' in request.POST:
        exercise_id = request.POST["epk"]
        exercise = Exercise.objects.get(pk = exercise_id)
        workout_id = request.POST["wpk"]
        workout = Workout.objects.get(pk = workout_id)
        exercises = Stored_Exercise.objects.all().order_by('name')
        context.update({'exercise':exercise,'workout':workout,'exercises':exercises})

    return render(request,'gymtracker/edit_exercise.html',context)

@verify_loggedin
def edit_exercise_processing(request,profile):
    context = {'appname': appname, 'logIn': True,}
    if 'exercise' in request.POST:
        ename = request.POST["exercise"]
        exercise_id = request.POST["epk"]
        exercise = Exercise.objects.get(pk = exercise_id)
        exercise.name = ename
        exercise.save()

        workout_id = request.POST["wpk"]
        workout = Workout.objects.get(pk = workout_id)
        exercises = Exercise.objects.filter(workout = workout).order_by('-created_at')
        context.update({'exercises':exercises, 'workout':workout})

    return render(request,'gymtracker/view_workout.html', context)


@verify_loggedin
def delete_exercise(request,profile):
    context = {'appname': appname, 'logIn': True,}
    if 'epk' in request.POST:
        exercise_id = request.POST["epk"]
        exercise = Exercise.objects.get(pk = exercise_id)
        exercise.delete()
        workout_id = request.POST["workout"]
        workout = Workout.objects.get(pk = workout_id)
        exercises = Exercise.objects.filter(workout=workout)
        context.update({'exercises':exercises, 'workout':workout})
    return render(request,'gymtracker/view_workout.html', context)



@verify_loggedin
def view_exercise(request,profile):
    context = {'appname': appname, 'logIn': True,}
    if 'epk' in request.POST:
        exercise_id = request.POST["epk"]
        print(exercise_id)
        exercise = Exercise.objects.get(pk = exercise_id)
        print(exercise)
        sets = Set.objects.filter(exercise=exercise)
        print(sets)

        context.update({'sets':sets, 'exercise':exercise})

    return render(request,'gymtracker/view_exercise.html', context)

@verify_loggedin
def add_set_later(request,profile):
    context = {'appname': appname, 'logIn': True,}
    if 'epk' in request.POST:
        exercise_id = request.POST["epk"]
        exercise = Exercise.objects.get(pk = exercise_id)
        context.update({'exercise':exercise})

        return render(request,'gymtracker/add_set.html',context)

@verify_loggedin
def edit_set(request,profile):
    context = {'appname': appname, 'logIn': True,}
    if 'spk' in request.POST:
        set_id = request.POST["spk"]
        set_ = Set.objects.get(pk = set_id)
        exercise_id = request.POST["epk"]
        exercise = Exercise.objects.get(pk = exercise_id)
        context.update({'exercise':exercise,'set':set_})

    return render(request,'gymtracker/edit_set.html',context)

@verify_loggedin
def edit_set_processing(request,profile):
    context = {'appname': appname, 'logIn': True,}
    if 'spk' in request.POST:
        set_id = request.POST["spk"]
        set_current = Set.objects.get(pk = set_id)

        set_no = request.POST["set_no"]
        reps = request.POST["reps"]
        weight = request.POST["weight"]

        set_current.set_no = set_no
        set_current.reps = reps
        set_current.weight = weight
        set_current.save()

        exercise_id = request.POST["epk"]
        exercise = Exercise.objects.get(pk = exercise_id)

        sets = Set.objects.filter(exercise = exercise)
        context.update({'sets':sets, 'exercise':exercise})

    return render(request,'gymtracker/view_exercise.html', context)

@verify_loggedin
def delete_set(request,profile):
    context = {'appname': appname, 'logIn': True,}
    if 'epk' in request.POST:
        exercise_id = request.POST["epk"]
        exercise = Exercise.objects.get(pk = exercise_id)
        exercise.delete()
        workout_id = request.POST["workout"]
        workout = Workout.objects.get(pk = workout_id)
        exercises = Exercise.objects.filter(workout=workout)
        context.update({'exercises':exercises, 'workout':workout})
    return render(request,'gymtracker/view_workout.html', context)

@verify_loggedin
def tutorials(request,profile):
    context = {'appname': appname, 'logIn': True,'exercise':None}
    exercises = Stored_Exercise.objects.all().order_by('name')
    context.update({'exercises':exercises})
    return render(request,'gymtracker/tutorials.html', context)

@verify_loggedin
def get_tutorial(request,profile):
    context = {'appname': appname, 'logIn': True,}
    exercise = request.POST['tutorials']
    exercises = Stored_Exercise.objects.all().order_by('name')
    sel_ex = Stored_Exercise.objects.get(name=exercise)
    context.update({'exercises':exercises,'exercise':exercise,'sel_ex':sel_ex})
    return render(request,'gymtracker/tutorials.html', context)

def tutorials_guest(request):
    context = {'appname': appname,'exercise':None}
    exercises = Stored_Exercise.objects.all().order_by('name')
    context.update({'exercises':exercises})
    return render(request,'gymtracker/tutorials_guest.html', context)

def get_tutorial_guest(request):
    context = {'appname': appname}
    exercise = request.POST['tutorials']
    exercises = Stored_Exercise.objects.all().order_by('name')
    sel_ex = Stored_Exercise.objects.get(name=exercise)
    context.update({'exercises':exercises,'exercise':exercise,'sel_ex':sel_ex})
    return render(request,'gymtracker/tutorials_guest.html', context)

#OneDrive\Desktop\CS\Year 3\Project\Implementation 2

