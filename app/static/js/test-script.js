var myElement = document.getElementById('myElement');

var mc = new Hammer(myElement);

//enable all directions
mc.get('swipe').set({
    direction: Hammer.DIRECTION_ALL,
    threshold: 1,
    velocity: 0.1
});

const goRight = () => {
    $('.gal-box.galcurr').each(function () {
        if ($(".gal-box:visible").next().length != 0) {
            $('.gal-box.galcurr').next('.gal-box').addClass('galcurr');
            $(this).removeClass('galcurr');
        } else {
            $(".gal-box:first").addClass('galcurr');
            $(".gal-box:last").removeClass('galcurr');
        }
    });
}

const goLeft = () => {
    $('.gal-box.galcurr').each(function () {
        if ($(".gal-box:visible").prev().length != 0) {
            $('.gal-box.galcurr').prev('.gal-box').addClass('galcurr');
            $(this).removeClass('galcurr');
        } else {
            $(".gal-box:last").addClass('galcurr');
            $(".gal-box:first").removeClass('galcurr');
        }
    });
}

mc.on("swipeleft", goRight);
mc.on("swiperight", goLeft);

document.onkeyup = e => {
    switch(e.key) {
        case 'ArrowLeft':
            goLeft()
            break
        
        case 'ArrowRight':
            goRight()
            break
        
        default:
            break
    }
}