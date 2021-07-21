document.addEventListener('DOMContentLoaded', function() {
    doesLike = document.querySelector('#does_like').textContent;

    likeButton = document.querySelector('#like-button');

    if (doesLike == "True") {
        likeButton.textContent = 'Unlike'
    }
    document.querySelector('#edit-view').style.display = 'none';

    document.querySelector('#edit-btn').addEventListener('click', () => {
        const post_id = window.location.pathname.split("/")[2];
        editPost(post_id);
    })
})

const editPost = (post_id) => {
    editButton = document.querySelector('#edit-btn');
    editButton.style.display = 'none'
    document.querySelector('#edit-view').style.display = 'block';
    
    document.querySelector('#compose-form').addEventListener('submit', () => {
        submitPost(post_id);
    });

    mailBodyTag = document.querySelector('#post-body');
    mailBody = mailBodyTag.textContent;

    document.querySelector('#edit-body').textContent = mailBody;

    mailBodyTag.style.display = 'none';
}

const submitPost = (post_id) => {
    fetch(`/post/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            post_id: post_id,
            new_body: document.querySelector('#edit-body').value
        })
    })
}

const like = (current_user, post_id) => {
    fetch(`/post/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            like: true,
            post_id: post_id,
            user_id: current_user
        })
    })

    likeButton = document.querySelector('#like-button');
    likes = document.querySelector('#likes');
    likeCount = parseInt(likes.textContent.split(" ")[1]);

    if (likeButton.textContent == 'Like') {
        likeButton.textContent = 'Unlike';
        likes.textContent = `likes: ${likeCount + 1}`
    } else {
        likeButton.textContent = 'Like';
        likes.textContent = `likes: ${likeCount - 1}`
    }

}