from .models import Following, Likes, User

def is_following(current_user, profile):
    user = Following.objects.get(user=current_user).user

    profile_user = Following.objects.get(user=profile)
    profile_user_followers = profile_user.followers.all()

    if user not in profile_user_followers:
        return False
    return True

def does_like(current_user, post_id):
    users_that_like_post = Likes.objects.get(post=post_id).users.all()

    user = User.objects.get(user=current_user)

    if user not in users_that_like_post:
        return False
    return True
    #return {"user": user.id, "users":users_that_like_post}



