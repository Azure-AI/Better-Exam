var myElement = document.getElementById('myElement');


var mc = new Hammer(myElement);

//enable all directions
mc.get('swipe').set({
  direction: Hammer.DIRECTION_ALL,
  threshold: 1, 
  velocity:0.1
});

// listen to events...

// swipeup swipedown swipeleft swiperight tap press



mc.on("swipeleft", function(ev) {
//   myElement.textContent = ev.type + " gesture detected.";
  $('.gal-box.galcurr').each(function () {
    if ($(".gal-box:visible").next().length != 0) {
        $('.gal-box.galcurr').next('.gal-box').addClass('galcurr');
        $(this).removeClass('galcurr');
    } else {
        $(".gal-box:first").addClass('galcurr');
        $(".gal-box:last").removeClass('galcurr');
    }
});
  
  
});


mc.on("swiperight", function(ev) {
    //   myElement.textContent = ev.type + " gesture detected.";
    $('.gal-box.galcurr').each(function () {
        if ($(".gal-box:visible").prev().length != 0) {
            $('.gal-box.galcurr').prev('.gal-box').addClass('galcurr');
            $(this).removeClass('galcurr');
        } else {
            $(".gal-box:last").addClass('galcurr');
            $(".gal-box:first").removeClass('galcurr');
        }
    });
      
      
    });








/* clicking next button */
$('.gal-tabs a.nxt').each(function () {
    console.log(this);
    $(this).click(function () {
        $('.gal-box.galcurr').each(function () {
            if ($(".gal-box:visible").next().length != 0) {
                $('.gal-box.galcurr').next('.gal-box').addClass('galcurr');
                $(this).removeClass('galcurr');
            } else {
                $(".gal-box:first").addClass('galcurr');
                $(".gal-box:last").removeClass('galcurr');
            }
        });
    });
});

/* clicking previous button */
$('.gal-tabs a.prv').each(function () {
    $(this).click(function () {
        $('.gal-box.galcurr').each(function () {
            if ($(".gal-box:visible").prev().length != 0) {
                $('.gal-box.galcurr').prev('.gal-box').addClass('galcurr');
                $(this).removeClass('galcurr');
            } else {
                $(".gal-box:last").addClass('galcurr');
                $(".gal-box:first").removeClass('galcurr');
            }
        });
    });
});


