document.addEventListener('DOMContentLoaded', function() {
    isFollowing = Boolean(document.querySelector('#is_following').textContent);

    followButton = document.querySelector('#follow_button');

    if (!isFollowing) {
        followButton.textContent = 'Unfollow'
    }
})
const follow = (current_user, profile, profile_id) => {
    fetch(`/profile/${profile_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            user: current_user,
            profile: profile
        })
    })

    followButton = document.querySelector('#follow_button');
    followers = document.querySelector('#followers');
    followerCount = parseInt(followers.textContent.split(" ")[1]);

    if (followButton.textContent == 'Follow') {
        followButton.textContent = 'Unfollow';
        followers.textContent = `followers: ${followerCount + 1}`
    } else {
        followButton.textContent = 'Follow';
        followers.textContent = `followers: ${followerCount - 1}`
    }

}