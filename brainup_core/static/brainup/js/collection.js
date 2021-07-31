$('document').ready(function(){
    $('.remove-button').on('click', function(){
        let element = $(this).parents('.flip-card');
        let card_id = element.data().cardId
        $.ajax({
            url: remove_url + card_id,
            type: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(result) {
                console.log('obj removed!')
                element.parent().remove()
            },
            error: function(err){
                console.error(err)
            }
        })
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
