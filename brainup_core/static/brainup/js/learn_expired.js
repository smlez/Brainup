$('document').ready(function(){
    console.log(collections_list)
    console.log(expired_cards)
    collections_list.forEach((collection) => {
        $('#collection-selector').append(`<option value=${collection[0]}>${collection[1]}</option>`)
    })
    $('#collection-selector').on('change', function(){
        let value = $(this).val()
        if (expired_cards[value] != []){
        $('#info-container p').text(`Карт для повторения в выбранной коллекции: ${expired_cards[value].length}`)
        console.log('t')

        }
    })
})