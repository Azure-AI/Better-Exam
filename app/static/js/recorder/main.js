/* Copyright 2013 Chris Wilson

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

window.AudioContext = window.AudioContext || window.webkitAudioContext;

var audioContext = new AudioContext();
var audioInput = null,
    realAudioInput = null,
    inputPoint = null,
    audioRecorder = null;
var rafID = null;
var analyserContext = null;
var canvasWidth, canvasHeight;
var recIndex = 0;

/* TODO:

- offer mono option
- "Monitor input" switch
*/

function saveAudio() {
    audioRecorder.exportWAV(doneEncoding);
}


function gotBuffers(buffers) {
    audioRecorder.exportWAV(doneEncoding);
}

function doneEncoding(blob) {
    Recorder.sendRecording(blob, "myRecording" + ((recIndex < 10) ? "0" : "") + recIndex + ".wav");
    recIndex++;
}

const stopRecording = e => {
    console.log('Recording stopped');
    audioRecorder.stop();
    e.classList.remove("recording");
    audioRecorder.getBuffers(gotBuffers);
    recordFinish.play()
}

const startRecording = e => {
    if (!audioRecorder)
        return;
    console.log('Recording started');
    e.classList.add("recording");
    audioRecorder.clear();
    audioRecorder.record();
    audioContext.resume();
}

function toggleRecording(e) {
    console.log("Hold detected!");
    if (e.classList.contains("recording")) {
        stopRecording(e)
    } else {
        recordStart.play()
    }
}


function gotStream(stream) {
    inputPoint = audioContext.createGain();

    // Create an AudioNode from the stream.
    realAudioInput = audioContext.createMediaStreamSource(stream);
    audioInput = realAudioInput;
    audioInput.connect(inputPoint);

    analyserNode = audioContext.createAnalyser();
    analyserNode.fftSize = 2048;
    inputPoint.connect(analyserNode);

    audioRecorder = new Recorder(inputPoint);

    zeroGain = audioContext.createGain();
    zeroGain.gain.value = 0.0;
    inputPoint.connect(zeroGain);
    zeroGain.connect(audioContext.destination);
}

function initAudio() {
    // if (!navigator.getUserMedia)
    //     navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    // if (!navigator.cancelAnimationFrame)
    //     navigator.cancelAnimationFrame = navigator.webkitCancelAnimationFrame || navigator.mozCancelAnimationFrame;
    // if (!navigator.requestAnimationFrame)
    //     navigator.requestAnimationFrame = navigator.webkitRequestAnimationFrame || navigator.mozRequestAnimationFrame;

    navigator.mediaDevices.getUserMedia({
        video: false,
        audio: true
    }).then(stream => {
        // window.localStream = stream; // A
        // window.localAudio.srcObject = stream; // B
        // window.localAudio.autoplay = true; // C
        gotStream(stream)
    }).catch(err => {
        alert('Error getting audio');
        console.log("u got an error:" + err)
    });
    // navigator.getUserMedia({
    //     "audio": {
    //         "mandatory": {
    //             "googEchoCancellation": "false",
    //             "googAutoGainControl": "false",
    //             "googNoiseSuppression": "false",
    //             "googHighpassFilter": "false"
    //         },
    //         "optional": []
    //     },
    // }, gotStream, function (e) {
    //     alert('Error getting audio');
    //     console.log(e);
    // });
}

window.addEventListener('load', initAudio);