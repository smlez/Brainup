$('document').ready(function(){
    $('.remove-button').on('click', function(){
        let element = $(this).parents('.flip-card');
        if (confirm(`Are you sure want to delete card ${element.data().front}?`)){
            $.ajax({
                url: remove_url + element.data().id,
                type: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function(result) {
                    element.parent().remove()
                },
                error: function(err){
                    console.error(err)
                }
            })
        }

    })
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
