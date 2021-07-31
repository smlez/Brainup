$('document').ready(function(){
    console.log('te')

    $('.back-card-div').each(function(){
        $(this).css('transform',`rotate( ${getRandom(-10,5)}deg)`)
    })
})

function getRandom(min, max){
    return Math.round(min + Math.random() * (max - min))
}