var myElement = document.getElementById('myElement');


var mc = new Hammer(myElement);

//enable all directions
mc.get('swipe').set({
  direction: Hammer.DIRECTION_ALL,
  threshold: 1, 
  velocity:0.1
});

// listen to events...
mc.on("swipeup swipedown swipeleft swiperight tap press", function(ev) {
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


/* displaying total length of gal-box class */
var galtotal = $('.gal-box').length;
$('.galtotal').html(galtotal);

/* adding attribute data-id that starts from 1 not 0 */
$('.gal-box').attr("data-id", function (index) {
    return (index + 1);
});

/* displaying data-id equivalent of gal-box class */
$('.gal-box').each(function () {
    if ($(this).hasClass('galcurr')) {
        return $('.galcount').html($(this).attr('data-id'));
    }
});

$('body').on('click', '.gal-tabs a', function (e) {
    e.preventDefault();
    $('.gal-box').each(function (i, obj) {
        if ($(this).hasClass('galcurr')) {
            return $('.galcount').html($(this).attr('data-id'));
        }
    });
});