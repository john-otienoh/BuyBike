$(window).scroll(function() {
    if ($(this).scrollTop() > 300) {
        $('.btt-button').fadeIn();
    } else {
        $('.btt-button').fadeOut();
    }
});

$('.btt-link').click(function(e) {
    e.preventDefault();
    $('html, body').animate({scrollTop: 0}, 500);
});

// AJAX sorting with loading indicator
$('#sort-selector').change(function() {
    const $selector = $(this);
    const $loading = $selector.siblings('.sort-loading');
    const currentUrl = new URL(window.location);
    const selectedVal = $selector.val();
    
    $loading.removeClass('d-none');
    
    if (selectedVal !== "reset") {
        const [sort, direction] = selectedVal.split('_');
        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");
    }
    
    // Reset pagination when sorting
    currentUrl.searchParams.delete("page");
    
    fetch(currentUrl, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        const $newContent = $(html).find('.product-container');
        $('.product-container').replaceWith($newContent);
        history.pushState({}, '', currentUrl);
    })
    .catch(() => {
        window.location.replace(currentUrl);
    })
    .finally(() => {
        $loading.addClass('d-none');
    });
});

$(document).on('click', '.delete-product', function(e) {
    e.preventDefault();
    const $button = $(this);
    $('#productName').text($button.data('product-name'));
    $('#confirmDelete').attr('href', $button.attr('href'));
    $('#deleteModal').modal('show');
});

$('.product-card').hover(
    function() {
        $(this).css('transform', 'translateY(-5px)');
        $(this).css('box-shadow', '0 10px 20px rgba(0,0,0,0.1)');
    },
    function() {
        $(this).css('transform', '');
        $(this).css('box-shadow', '');
    }
);
