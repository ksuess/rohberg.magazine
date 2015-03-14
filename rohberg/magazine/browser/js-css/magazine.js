$(document).ready(function() {
    
    $('a > .magnify').parent().prepOverlay({
             subtype: 'ajax',
             filter: '#content > *'
             });
    
    $('img.headerImage')
        .prepOverlay({
            subtype: 'image',
            urlmatch: 'headerimage$',
            urlreplace: 'headerimage'
            });
    $('div.photoAlbumEntry a')
        .prepOverlay({
            subtype: 'image',
            urlmatch: 'view$',
            urlreplace: '@@images/image/large'
            });
    

    // Icons
    $("a.url").prev('img').hide();
            
});