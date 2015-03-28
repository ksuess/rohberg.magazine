function load_flyout_grandchildren(indicator, open) {
  var me = indicator.children("a:first");
  var parent = me.parent('li');

  // hide all but this children
  var others = parent.siblings();
  others.find('ul').hide();
  others.removeClass('flyoutActive');

  var children = parent.find('ul:first');
  if (children.length == 0) {
      if (open) {
          $.ajax({
            type : 'GET',
            url : me.attr('href') + '/load_flyout_children',
            success : function(data, textStatus, XMLHttpRequest) {
              if (textStatus == 'success') {
                var result = $(data);
                if (result.find("li.level1").length >= 1) {
                    result.show();
                    parent.removeClass('loading');
                    parent.append(result);
                };
              }
            }
          });
      };
  } else {
      children.toggle();
  };
  if(open) {
    parent.toggleClass('flyoutActive');
  }

};

function load_flyout_children_urdorf(indicator, open) {
    // Kopie von plonetheme.onegov
    var me = indicator;
    var parent = me.parent('.wrapper').parent('li');

    // hide all but this children
    var others = $('#portal-globalnav li').not('#'+parent.attr('id'));
    others.find('ul').hide();
    others.removeClass('flyoutActive');

    var children = parent.find('ul:first');
    if (children.length == 0) {
      $.ajax({
        type : 'GET',
        url : me.attr('href') + '/load_flyout_children',
        success : function(data, textStatus, XMLHttpRequest) {
          if (textStatus == 'success') {
            var result = $(data);
            result.hide();
            parent.removeClass('loading');
            parent.append(result);
    
            // flyout navigation 2nd level
            parent.find('.level1').hover(function(e){
              e.preventDefault();
              load_flyout_grandchildren($(this), true);
            }, function(e){
              e.preventDefault();
              load_flyout_grandchildren($(this), false);
            });
            
            
          }
        }
      });
    }
    if(open) {
      parent.toggleClass('flyoutActive');
    }
    children.toggle();
};




$(document).ready(function() {

    $('#portal-globalnav.flyoutEnabled > li > .wrapper a').each(function(idx, el){
      load_flyout_children_urdorf($(el), false);
    });
    
    
    
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


