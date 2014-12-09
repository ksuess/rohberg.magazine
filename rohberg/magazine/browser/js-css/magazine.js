$(document).ready(function() {
    
    $('a > .magnify').parent().prepOverlay({
             subtype: 'ajax',
             filter: '#content > *'
             });
    
    $('img.headerImage')
        .prepOverlay({
            subtype: 'image',
            urlmatch: 'headerimage$',
            urlreplace: 'large'
            });
    
});