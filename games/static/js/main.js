function addDragEvents(fromSelector, toSelector) {
    var draggedItem;
    $(fromSelector).on('dragstart', function(e) {
        draggedItem = e.target;
    });
    $(toSelector).on('dragover', function(e) {
        e.preventDefault();
    });
    $(toSelector).on('drop', function(e) {
        console.log(e);
        e.preventDefault();
        e.target.appendChild(draggedItem);
        draggedItem = null;
    });
}


$(document).ready(function() {
    addDragEvents('#hand .card', '#played-cards');
});
