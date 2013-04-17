/********************************************************
 *
 * Custom Javascript code for Bootstrap theme
 * Inspired by Themelize.me (http://themelize.me)
 *
 *******************************************************/

// Return boolean TRUE/FALSE
var isiPhone = navigator.userAgent.match(/iPhone/i) != null;
if(isiPhone == 1) {
 // Hide Adress-Bar on iPhone
  window.addEventListener("load",function() {
    // Set a timeout...
    setTimeout(function(){
      // Hide the address bar!
      window.scrollTo(0, 1);
    }, 0);
  });
}


$(document).ready(function() {
  //var defaultColour = 'green';

  //Bootstrap tooltip
  // invoke by adding _tooltip to a tags (this makes it validate)
  $('body').tooltip({
    selector: "a[class*=_tooltip]"
  });

  // Bootstrap Carousel
  $('.carousel').carousel({
      /* interval: 3000 */
  })
    
  //Bootstrap popover
  // invoke by adding _popover to a tags (this makes it validate)
  $('body').popover({
    selector: "a[class*=_popover]",
    trigger: "hover"
  });
  
  //show hide elements
  $('.show-hide').each(function() {
    $(this).click(function() {
      var state = 'open'; //assume target is closed & needs opening
      var target = $(this).attr('data-target');
      var targetState = $(this).attr('data-target-state');
      
      //allows trigger link to say target is open & should be closed
      if (typeof targetState !== 'undefined' && targetState !== false) {
        state = targetState;
      }
      
      if (state == 'undefined') {
        state = 'open';
      }
      
      $(target).toggleClass('show-hide-'+ state);
      $(this).toggleClass(state);      
    });
  });
  
  
  //external links
  $("a").filter(function() {
      return this.hostname &&
             this.hostname.replace(/^www\./, '') !==
                location.hostname.replace(/^www\./, '');
  }).each(function() {
     if (!$(this).hasClass("no-ico")) {
	     $(this).attr({
	         target: "_blank",
	         title: "Visit " + this.href + " (click to open in a new window)"
	      });
	      var text = $(this).text();
	      $(this).html(text +' <i class="icon-external-link"></i>');
     }
  });
      
  
  
  /*
  //flexslider
  $('.flexslider').each(function() {
    var sliderSettings =  {
      animation: $(this).attr('data-transition'),
      selector: ".slides > .slide",
      controlNav: true,
      smoothHeight: true
    };
    
    var sliderNav = $(this).attr('data-slidernav');
    if (sliderNav != 'auto') {
      sliderSettings = $.extend({}, sliderSettings, {
        manualControls: sliderNav +' li a',
        controlsContainer: '.flexslider-wrapper'
      });
    }
    
    $(this).flexslider(sliderSettings);
  }); 
  */  

  //jQuery Quicksand plugin
  //@based on: http://www.evoluted.net/thinktank/web-development/jquery-quicksand-tutorial-filtering
  var $filters = $('#quicksand-categories');
  var $filterType = $filters.find('li.active a').attr('class');
  var $holder = $('ul#quicksand');
  var $data = $holder.clone();

  // react to filters being used
  $filters.find('li a').click(function(e) {
    $filters.find('li').removeClass('active');
    var $filterType = $(this).attr('class');
    $(this).parent().addClass('active');
    if ($filterType == 'all') {
      var $filteredData = $data.find('li');
    } 
    else {
      var $filteredData = $data.find('li[data-type=' + $filterType + ']');
    }

    // call quicksand and assign transition parameters
    $holder.quicksand($filteredData, {
      duration: 800,
    });
    e.preventDefault();
  });
  
 


  // RESPONSIVE VIDEO CODES
  $(function() {
      
      var $allVideos = $("iframe[src^='http://player.vimeo.com'], iframe[src^='http://www.youtube.com'], object, embed"),
      $fluidEl = $("figure");
          
    $allVideos.each(function() {
    
      $(this)
        // jQuery .data does not work on object/embed elements
        .attr('data-aspectRatio', this.height / this.width)
        .removeAttr('height')
        .removeAttr('width');
    
    });
    
    $(window).resize(function() {
    
      var newWidth = $fluidEl.width();
      $allVideos.each(function() {
      
        var $el = $(this);
        $el
            .width(newWidth)
            .height(newWidth * $el.attr('data-aspectRatio'));
      
      });
    
    }).resize();
  
  });


  
});