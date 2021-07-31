let cards_collected = []


$('document').ready(function(){
         $.ajax({
        type: 'GET',
        url: api_url,
        dataType : 'json',
        success: function(data){
            data.forEach(el => {cards_collected.push(el)})
        }})
        //заполнить коллекциями чекер
        //загрузить шаблон карточки из card.html в cards-block

})

function container_changed(){

}

function collection_changed(){
    console.log(cards_collected)
}