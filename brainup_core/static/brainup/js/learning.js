var cards = collection.cards
var knowing_buttons = document.getElementById("knowing-buttons")
var isFirstLearning = true
var unknown_cards = []
var today = new Date()
var is_back_side = false
var current_card_id = 0


$(document).ready(() => {
    write_card_data(0)
    console.log(cards)
    var zIndex = 0
    $('.card-side').on('click', function(){
        $(this).toggleClass('is-flipped')
    })
})

function turn_front_func(){
    console.log('front turned')
    is_back_side = true
}

function turn_back_func(){
    console.log('back turned')
    is_back_side = false
}

function write_card_data(id){
    $('#card-front-content').text(cards[id].front_side)
    $('#card-back-content').text(cards[id].back_side)
}

function answer_on_question(isKnow){
    if(current_card_id==cards.length-1){
        end_game()
        return
    }
        card = cards[current_card_id]
        if (isKnow){
            if (card.knowledge <= 5){
                card.knowledge = (Number.parseInt(card.knowledge) + 1).toString()
                card.entry_date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate()
            }
            } else {
                if (card.knowledge > 3)
                    card.knowledge = (card.knowledge - 2).toString()
                else
                    card.knowledge = "1"
            }
            if(is_back_side) {
                    $('.card-side').toggleClass('is-flipped')
                    is_back_side = false
                }
            current_card_id++
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



function end_game(){

    alert('Congratulations! You have learned this collection')
    $.ajax({
        url: collection_url + collection.id + '/' ,
        type: 'PATCH',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        contentType: "application/json",
        data: JSON.stringify({ cards: cards }),
        success: function(data)  {
            console.log(data)
        },
        error: function(data){
            console.log('error');
            console.log(data);
        }
    })
    location.href = '/'
}











