from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signup_processing', views.signup_processing, name='signup_processing'),
    path('signin', views.signin, name='signin'),
    path('signin_processing', views.signin_processing, name='signin_processing'),
    path('signout', views.signout, name='signout'),
    path('verify_loggedin', views.verify_loggedin, name='verify_loggedin'),
    
    path('friends', views.friends, name='friends'),
    path('search_friend', views.search_friend, name='search_friend'),
    path('display_searched_user', views.display_searched_user, name='display_searched_user'),
    path('add_friend', views.add_friend, name='add_friend'),
    path('remove_friend', views.remove_friend, name='remove_friend'),
    path('show_all_followings', views.show_all_followings, name='show_all_followings'),
    path('following_record', views.following_record, name='following_record'),
    path('remove_friend_2', views.remove_friend_2, name='remove_friend_2'),

    path('view_following_workout', views.view_following_workout, name='view_following_workout'),#view exercises within a workout for a select followed user
    path('view_following_exercise', views.view_following_exercise, name='view_following_exercise'),#view sets within an exercise for a select followed user


    path('add_workout', views.add_workout, name='add_workout'),
    path('add_workout_processing', views.add_workout_processing, name='add_workout_processing'),
    path('add_exercise', views.add_exercise, name='add_exercise'),
    path('add_exercise_processing', views.add_exercise_processing, name='add_exercise_processing'),
    path('add_set', views.add_set, name='add_set'),
    path('add_set_processing', views.add_set_processing, name='add_set_processing'),

    path('record', views.record, name='record'),#display all workouts
    path('edit_workout', views.edit_workout, name='edit_workout'),
    path('edit_workout_processing', views.edit_workout_processing, name='edit_workout_processing'),#edit a workout entry
    
    path('delete_workout', views.delete_workout, name='delete_workout'),#delete workout

    path('view_workout', views.view_workout, name='view_workout'),#view exercises within a workout
    path('add_exercise_later',views.add_exercise_later, name='add_exercise_later'),
    path('edit_exercise', views.edit_exercise, name='edit_exercise'),
    path('edit_exercise_processing', views.edit_exercise_processing, name='edit_exercise_processing'),#edit a exercise entry
    path('delete_exercise', views.delete_exercise, name='delete_exercise'),#delete exercise

    path('view_exercise', views.view_exercise, name='view_exercise'),#view sets within a exercise
    path('add_set_later',views.add_set_later, name='add_set_later'),
    path('edit_set', views.edit_set, name='edit_set'),
    path('edit_set_processing', views.edit_set_processing, name='edit_set_processing'),#edit a set entry
    path('delete_set', views.delete_set, name='delete_set'),#delete set

    path('tutorials', views.tutorials, name='tutorials'),
    path('get_tutorial', views.get_tutorial, name='get_tutorial'),
    path('tutorials_guest', views.tutorials_guest, name='tutorials_guest'),
    path('get_tutorial_guest', views.get_tutorial_guest, name='get_tutorial_guest'),
]
