var myElement = document.getElementById('myElement');

var clicked_id;
var audio_var = new Audio();

const recordStart = document.createElement('audio')
recordStart.setAttribute('src', '/static/asset/audio/rec-start.mp3')

recordStart.onended = () => {
    startRecording(myElement)
}

const recordFinish = document.createElement('audio')
recordFinish.setAttribute('src', '/static/asset/audio/rec-finish.mp3')

const answerSubmit = document.createElement('audio')
answerSubmit.setAttribute('src', '/static/asset/audio/ans-submit.mp3')

const nameSubmit = document.createElement('audio')
nameSubmit.setAttribute('src', '/static/asset/audio/name-submit.mp3')

const examTerminate = document.createElement('audio')
examTerminate.setAttribute('src', '/static/asset/audio/exam-terminate.mp3')

const audios = [recordStart, recordFinish, answerSubmit, nameSubmit, examTerminate]
let audiosToBeLoaded = audios.length

for (const audioFile of audios) {
    audioFile.oncanplaythrough = () => {
        if (--audiosToBeLoaded == 0) {
            console.log('All loaded');
        }
    }
}

var mc = new Hammer(myElement);

//enable all directions
mc.get('swipe').set({
    direction: Hammer.DIRECTION_ALL,
    threshold: 1,
    velocity: 0.1
});

mc.get('press').set({
    time: 1000
})

const terminateExam = () => {
    $.ajax({
        type: 'POST',
        beforeSend: function (request) {
            request.setRequestHeader("token-id", localStorage.getItem('token-id'));
        },
        url: 'terminate',
        processData: false,
        contentType: false
    }).done(_ => {
        examTerminate.play()
    })
}

const goRight = () => {
    if ($('.gal-box:visible').attr('islastpage') === 'true') {
        console.log('Finalizing exam');
        terminateExam()
    } else {
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
    
                console.log('GO RIGHT');
                $('.gal-box.galcurr').next('.gal-box').addClass('galcurr');
                $(this).removeClass('galcurr');
            } else {
                $(".gal-box:first").addClass('galcurr');
                $(".gal-box:last").removeClass('galcurr');
            }
        });   
    }
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



function hello() {
    // alert("hi")
    goRight()
}

$(function () {
    $('div[onload]').trigger('onload');
});

mc.on("swipeleft", goRight);
mc.on("swiperight", goLeft);
mc.on("press", () => toggleRecording(myElement))
// mc.on("doubletap", repeat);

mc.on('doubletap', function (e) {

    let audio = $('.gal-box.galcurr').find('.ppbutton')
    let datasrc = audio.attr('data-src');
    clicked_id = audio.attr('id');
    console.log(clicked_id);
    audio_var.pause();
    audio_var.src = datasrc;
    audio_var.play();

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