$('document').ready(function(){
    $('.back-card-div').each(function(){
        $(this).css('transform',`rotate( ${getRandom(-10,5)}deg)`)
    })
    $('.remove-button').on('click', function(){
        element = $(this).parents('.cards-container-div')
        if (confirm(`Are you sure want to remove collection ${element.data().title}?`)){
            $.ajax({
            url: collection_api_url + element.data().id,
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
    $('.empty-collection').on('click', function(){
        $('.modal-card-creation').css({'display': 'block'})
    })
    $('.modal-card-creation').on('mousedown', function(event){
        if (event.target.className == 'modal-card-creation' || event.target.className == 'close-modal-cross')
            $(this).css({'display': 'none'})
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

function getRandom(min, max){
    return Math.round(min + Math.random() * (max - min))
}

