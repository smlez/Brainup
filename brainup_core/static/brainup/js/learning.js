let originalCards = collection;
let currentCards = originalCards;
let unknown_cards = [];
let isRepeatingAll = true;
let today = new Date();
let is_back_side = false;
let current_card_id = 0;


$(document).ready(() => {
    console.log(currentCards)
    currentCards.sort(function (a, b) {
        if (a['cards__knowledge'] < b['cards__knowledge'])
            return -1
        else return 1
    })
    console.log(currentCards)
    write_card_data(0)
})

function turn_card(isTurnOnce) {
    if (isTurnOnce){
        is_back_side = !is_back_side
        $('.card-side').removeClass('is-flipped-twice')
        $('.card-side').toggleClass('is-flipped')
    } else {
        $('.card-side').toggleClass('is-flipped-twice')
    }
}

function write_card_data(id) {
    $('#card-front-content').text(currentCards[id]['cards__front_side'])
    $('#card-back-content').text(currentCards[id]['cards__back_side'])
}

function answer_on_question(isKnow) {
    let card = currentCards[current_card_id]
    if (isRepeatingAll) {
        if (isKnow) {
            if (card['cards__knowledge'] <= 5) {
                card['cards__knowledge'] = (Number.parseInt(card['cards__knowledge']) + 1).toString()
                card['cards__entry_date'] = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate()
            }

        } else {
            unknown_cards.push(card)
            if (card['cards__knowledge'] > 3)
                card['cards__knowledge'] = (card['cards__knowledge'] - 2).toString()
            else
                card['cards__knowledge'] = "1"
        }

    } else {
        if (isKnow) currentCards.splice(current_card_id, 1)
    }
    current_card_id++
    console.log(current_card_id)
    if (current_card_id >= currentCards.length) {
        if (unknown_cards.length === 0) {
            end_game()
            return
        } else {
            if (!isRepeatingAll) {
                current_card_id = 0
            } else {
                isRepeatingAll = false
                currentCards = unknown_cards
            }
        }
        current_card_id = 0
    }
    if (is_back_side)
        turn_card(true)
    else
        turn_card(false)
    write_card_data(current_card_id)
}

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

function end_game() {

    alert('Congratulations! You have learned this collection')
    $.ajax({
        url: collection_url + collection.id + '/',
        type: 'PATCH',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        contentType: "application/json",
        data: JSON.stringify({cards: originalCards}),
        success: function (data) {
            console.log(data)
        },
        error: function (data) {
            console.log('error');
            console.log(data);
        }
    })
    location.href = '/'
}











