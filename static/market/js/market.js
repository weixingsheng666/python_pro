$(function () {
    $('market').width(innerWidth)

    typeIndex = $.cookie('typeIndex')
    if(typeIndex){
        $('.type-slider  .type-item').eq(typeIndex).addClass('active')

    }else {
        $('.type-slider  .type-item:first').addClass('active')
    }


    $('.type-slider  .type-item').click(function () {

        // console.log($(this).index())

        $.cookie('typeIndex', $(this).index(), {exprires: 3, path:'/'})

    })




    var alltypebt = false
    var allsortbt = false

    $('#allbt').click(function () {
        alltypebt = !alltypebt

        if (alltypebt){

             $('.bounce-view.type-view').show()
             $('#allbt b').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')


             allsortbt = !allsortbt
             $('.bounce-view.sort-view').hide()
             $('#sortbt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')


        }else {
             $('.bounce-view.type-view').hide()
             $('#allbt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        }

    })




    $('#sortbt').click(function () {
        allsortbt = !allsortbt

        if (allsortbt) {

             $('.bounce-view.sort-view').show()
             $('#sortbt b').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')


             alltypebt = !alltypebt
             $('.bounce-view.type-view').hide()
             $('#allbt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        } else {
            $('.bounce-view.sort-view').hide()
            $('#sortbt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        }

    })

})