// Get full document height
$.getDocHeight = function(){
    return Math.max(
        $(document).height(),
        $(window).height(),
        /* For opera: */
        document.documentElement.clientHeight
    );
};

// Fires when user scrolled to the bottom end
$.bottomReached = function(){
    return ($(window).scrollTop() + $(window).height() == $.getDocHeight());
};

// If user scrolled down to the bottom end - request new page
$(window).scroll(function(){
    if ($.bottomReached()) {
        $.getPage();
    }
})

// Insert received page in the article container
$.insertPage = function(response){
    $('#article-container').append(response);
};

// Needed to proper work of coroutine and yield
function coroutine(f) {
    var o = f(); // instantiate the coroutine
    o.next(); // execute until the first yield
    return function(x) {
        o.next(x);
    }
}

// Get new page in ajax request
// Maximum number of pages on the site - 100
$.getPage = coroutine(function*(){
    for (i=1; i<100; i++) {
        yield;
        $.ajax({
            type: 'GET',
            url: '/get_page/',
            data: {
                'page': i
            },
            dataType: 'html',
            success: $.insertPage
        });
    }
});

// Get first page after document is loaded
$(document).ready(function(){
    $.getPage();
});