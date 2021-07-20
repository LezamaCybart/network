document.addEventListener('DOMContentLoaded', function() {
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
