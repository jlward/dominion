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


$(document).ready(function() {
    addDragEvents('#hand .card', '#played-cards');
});
