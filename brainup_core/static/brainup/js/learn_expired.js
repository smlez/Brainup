$('document').ready(function(){
    collections_list.forEach((collection) => {
        $('#collection-selector').append(`<option value=${collection[0]}>${collection[1]}</option>`)
    })
    $('#collection-selector').on('change', function(){
        let value = $(this).val()
        let p_container = $('#info-container p')
        if (value>-1)
            write_cards_count(p_container, expired_cards[value].length)
        else
            write_cards_count(p_container, amount_expired_cards)
    })
    $('#start-learn-button').on('click', function(){
        let cards_list = []
        let selector_value = $('#collection-selector').val()
        if (selector_value != -1){
            cards_list = expired_cards[selector_value]
        } else {
            for (key in expired_cards) {cards_list = cards_list.concat(expired_cards[key]) }
        }
        console.log(cards_list)
    })
})

function write_cards_count(element, count){
    element.text(`Карт для повторения в выбранной коллекции: ${count}`)
}