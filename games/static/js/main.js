function addDragEvents(fromSelector, toSelector) {
    var draggedItem;
    $(fromSelector).on('dragstart', function(e) {
        draggedItem = $(e.target);
    });
    $(toSelector).on('dragover', function(e) {
        e.preventDefault();
    });
    $(toSelector).on('drop', function(e) {
        console.log(e);
        console.log(draggedItem.data());
        e.preventDefault();
        // e.target.appendChild(draggedItem);
        // draggedItem = null;
        $csrfToken = $('span.csrf_token input');
        tokenName = $csrfToken.attr('name');
        if (draggedItem.data('url') === undefined){
            return
        }
        $.ajax({
            type: "post",
            url: draggedItem.data('url'),
            datatype: 'application/json',
            data: {
                'card': draggedItem.data('name'),
            },
            headers: {'X-CSRFToken': $csrfToken.val()},
            mode: 'same-origin',
            success: function(data){
                if(data.okay){
                    location.reload();
                }
            }
        });
    });
}

function allowBuyKingdomCard(){
    $('#body .card').on('click', function(e){
        $card = $(e.target);
        $('#buyModal span#cardName').text($card.data('name'));
        $clonedImg = $card.clone();
        $clonedImg.find('.count').remove();
        $('#buyModal span#cardImg').empty();
        $('#buyModal span#cardImg').append($clonedImg);
        $('#buyModal .btn-confirm').on('click', function(e){
            $csrfToken = $('span.csrf_token input');
            tokenName = $csrfToken.attr('name');
            if ($card.data('url') === undefined){
                return
            }
            $.ajax({
                type: "post",
                url: $card.data('url'),
                datatype: 'application/json',
                data: {
                    'card': $card.data('name'),
                },
                headers: {'X-CSRFToken': $csrfToken.val()},
                mode: 'same-origin',
                success: function(data){
                    if(data.okay){
                        location.reload();
                    }
                }
            });
        })
        $('#buyModal').modal();
    })
}

function autoReload(){
    $info = $('#gameHash');
    if($info.data('turn') === 1){
        return
    }
    if($info.data('over') === 1){
        return
    }
    function checkHash(){
        $.ajax({
            type: "get",
            datatype: 'application/json',
            url: $info.data('url'),
            success: function(data){
                if(data.hash != $info.data('hash')){
                    location.reload();
                }
            }
        });
    }
    setInterval(checkHash, 1000);
}

function autoOn(){
    modal = $('.auto-on');
    modal.modal('show');
}

$(document).ready(function() {
    addDragEvents('#hand .card', '#played-cards');
    allowBuyKingdomCard();
    autoReload();
    autoOn();
});
