$('document').ready(function(){
    let amount_expired_cards = 0
    let holder = $('#number-holder-2')
    let collection_selector = $('#collection-selector')

    collections_list.forEach((collection) => {
        collection_selector.append(`<option value=${collection['id']} data-count=${collection['cards__id__count']}>${collection['title']}</option>`)
        amount_expired_cards += collection['cards__id__count']
    })
    $('#collection-selector option:nth-child(1)').data('count', amount_expired_cards)
    console.log($('#collection-selector option:nth-child(1)').val())
    console.log($('#collection-selector option:nth-child(1)').data())

    $('#number-holder-1').text(amount_expired_cards)
    holder.text(amount_expired_cards)

    collection_selector.on('change', function(){
        let value = $(this).find(':selected').data('count')
        holder.text(value)
    })

    $('#start-learn-button').on('click', function(){
          $.get(redirect_url, {'id': collection_selector.val()})
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