var yeller = document.getElementById('yeller');
var canvas = document.getElementById('canvas');

yeller.innerHTML = 'This is events';

var hammertime = new Hammer(canvas);
hammertime.get('swipe').set({
    direction: Hammer.DIRECTION_ALL
});


var vw = window.innerWidth;
var vh = window.innerHeight;
var currentXPos = 0;
var currentYPos = 0;
var aniSpeed = 0.4;

let swipeleft = () => {
    yeller.innerHTML = 'swipeleft';
    currentXPos -= vw;
    TweenMax.to('#blockwrapper', aniSpeed, {
        x: currentXPos,
        ease: Back.easeOut
    })
}

let swiperight = () => {
    yeller.innerHTML = 'swiperight';
    currentXPos += vw;
    TweenMax.to('#blockwrapper', aniSpeed, {
        x: currentXPos,
        ease: Back.easeOut
    })
}

let swipeup = () => {
    yeller.innerHTML = 'swipeup';
    currentYPos -= vh;
    TweenMax.to('#blockwrapper', aniSpeed, {
        y: currentYPos,
        ease: Back.easeOut
    })
}

let dragup = () => {
    yeller.innerHTML = 'dragup';
    currentYPos -= vh;
    TweenMax.to('#blockwrapper', aniSpeed, {
        y: currentYPos,
        ease: Back.easeOut
    })
}
let swipedown = () => {
    yeller.innerHTML = 'swipedown';
    currentYPos += vh;
    TweenMax.to('#blockwrapper', aniSpeed, {
        y: currentYPos,
        ease: Back.easeOut
    })
}

hammertime.on("swipeleft", swipeleft);
hammertime.on("swiperight", swiperight);
hammertime.on("swipeup", swipeup);
hammertime.on("swipedown", swipedown);
hammertime.on("dragup", dragup);

document.onkeydown = (e => {
    switch(e.key) {
        case 'ArrowLeft':
            swiperight()
            break
        case 'ArrowRight':
            swipeleft()
            break
    }
})