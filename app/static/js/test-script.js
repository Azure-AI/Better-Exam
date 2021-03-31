var myElement = document.getElementById('myElement');

var clicked_id;
var audio_var = new Audio();


var mc = new Hammer(myElement);

//enable all directions
mc.get('swipe').set({
    direction: Hammer.DIRECTION_ALL,
    threshold: 1,
    velocity: 0.1
});

const goRight = ev => {
    console.log("right");
    $('.gal-box.galcurr').each(function () {
        if ($(".gal-box:visible").next().length != 0) {

            let audio = $('.gal-box.galcurr').next('.gal-box').find('.ppbutton')


            var datasrc = audio.attr('data-src');
            clicked_id = audio.attr('id');
            console.log(clicked_id);
            audio_var.pause();

            $('.ppbutton').not(audio).each(function () {
                $(this).removeClass('fa-pause');
                $(this).addClass('fa-play');
            });

            if (audio.hasClass('fa-play')) {
                console.log('play_click');
                audio_var.src = datasrc;
                audio.removeClass('fa-play');
                audio.addClass('fa-pause');
                console.log(audio_var);
                audio_var.play();
            } else {
                console.log('pause_click');
                audio.removeClass('fa-pause');
                audio.addClass('fa-play');
                console.log(audio_var);
                audio_var.pause();
                //audio_var.src='';
                //audio_var.load();
                console.log(audio_var);
            }

            console.log(audio.attr('id'));

            $('.gal-box.galcurr').next('.gal-box').addClass('galcurr');
            $(this).removeClass('galcurr');
        } else {
            $(".gal-box:first").addClass('galcurr');
            $(".gal-box:last").removeClass('galcurr');
        }
    });
}

const goLeft = () => {
    console.log("left");
    $('.gal-box.galcurr').each(function () {
        if ($(".gal-box:visible").prev().length != 0) {

            let audio = $('.gal-box.galcurr').prev('.gal-box').find('.ppbutton')


            var datasrc = audio.attr('data-src');
            clicked_id = audio.attr('id');
            console.log(clicked_id);
            audio_var.pause();

            $('.ppbutton').not(audio).each(function () {
                $(this).removeClass('fa-pause');
                $(this).addClass('fa-play');
            });

            if (audio.hasClass('fa-play')) {
                console.log('play_click');
                audio_var.src = datasrc;
                audio.removeClass('fa-play');
                audio.addClass('fa-pause');
                console.log(audio_var);
                audio_var.play();
            } else {
                console.log('pause_click');
                audio.removeClass('fa-pause');
                audio.addClass('fa-play');
                console.log(audio_var);
                audio_var.pause();
                //audio_var.src='';
                //audio_var.load();
                console.log(audio_var);
            }

            console.log(audio.attr('id'));

            $('.gal-box.galcurr').prev('.gal-box').addClass('galcurr');
            $(this).removeClass('galcurr');
        } else {
            $(".gal-box:last").addClass('galcurr');
            $(".gal-box:first").removeClass('galcurr');
        }
    });
}


const repeat = () => {
    console.log("repeat");
    $('.gal-box.galcurr').each(function () {

        alert("doublet tap")
        let audio = $('.gal-box.galcurr').find('.ppbutton')


        var datasrc = audio.attr('data-src');
        clicked_id = audio.attr('id');
        console.log(clicked_id);
        audio_var.pause();

        $('.ppbutton').not(audio).each(function () {
            $(this).removeClass('fa-pause');
            $(this).addClass('fa-play');
        });

        if (audio.hasClass('fa-play')) {
            console.log('play_click');
            audio_var.src = datasrc;
            audio.removeClass('fa-play');
            audio.addClass('fa-pause');
            console.log(audio_var);
            audio_var.play();
        } else {
            console.log('pause_click');
            audio.removeClass('fa-pause');
            audio.addClass('fa-play');
            console.log(audio_var);
            audio_var.pause();
            //audio_var.src='';
            //audio_var.load();
            console.log(audio_var);
        }

        console.log(audio.attr('id'));



    });
}


mc.on("swipeleft", goRight);
mc.on("swiperight", goLeft);
// mc.on("doubletap", repeat);

mc.on('doubletap', function (e) {

    let audio = $('.gal-box.galcurr').find('.ppbutton')
    let datasrc = audio.attr('data-src');
    clicked_id = audio.attr('id');
    console.log(clicked_id);
    audio_var.pause();
    audio_var.src = datasrc;
    audio_var.play();
    // alert(clicked_id)

    // $('.ppbutton').not(audio).each(function () {
    //     $(this).removeClass('fa-pause');
    //     $(this).addClass('fa-play');
    // });

    // if (audio.hasClass('fa-play')) {
    //     console.log('play_click');
    //     audio_var.src = datasrc;
    //     audio.removeClass('fa-play');
    //     audio.addClass('fa-pause');
    //     console.log(audio_var);
    //     audio_var.play();
    // } else {
    //     console.log('pause_click');
    //     audio.removeClass('fa-pause');
    //     audio.addClass('fa-play');
    //     console.log(audio_var);
    //     audio_var.pause();
    //     //audio_var.src='';
    //     //audio_var.load();
    //     console.log(audio_var);
    // }

    console.log(audio.attr('id'));

});

document.onkeyup = e => {
    switch (e.key) {
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






// /* clicking next button */
// $('.gal-tabs a.nxt').each(function () {
//     console.log(this);
//     $(this).click(function () {
//         $('.gal-box.galcurr').each(function () {
//             if ($(".gal-box:visible").next().length != 0) {
//                 $('.gal-box.galcurr').next('.gal-box').addClass('galcurr');
//                 $(this).removeClass('galcurr');
//             } else {
//                 $(".gal-box:first").addClass('galcurr');
//                 $(".gal-box:last").removeClass('galcurr');
//             }
//         });
//     });
// });

// /* clicking previous button */
// $('.gal-tabs a.prv').each(function () {
//     $(this).click(function () {
//         $('.gal-box.galcurr').each(function () {
//             if ($(".gal-box:visible").prev().length != 0) {
//                 $('.gal-box.galcurr').prev('.gal-box').addClass('galcurr');
//                 $(this).removeClass('galcurr');
//             } else {
//                 $(".gal-box:last").addClass('galcurr');
//                 $(".gal-box:first").removeClass('galcurr');
//             }
//         });
//     });
// });