from .models import Following

def is_following(current_user, profile):
    user = Following.objects.get(user=current_user).user

    profile_user = Following.objects.get(user=profile)
    profile_user_followers = profile_user.followers.all()

    if user not in profile_user_followers:
        return False
    return True
