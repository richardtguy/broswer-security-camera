const player = document.getElementById('player');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const constraints = {
  video: true,
};
var mediaRecorder = undefined;

// SocketIO connection
const peerConnections = {}
const config = {
  iceServers : [
    {
      urls: ["stun:stun.l.google.com:19302"]
    }
  ]
};
const socket = io();
socket.on('connect', () => {
  console.log('Connected to signal server');
});
// Handle new peer connections
socket.on('watcher', id => {
  const peerConnection = new RTCPeerConnection(config);
  peerConnections[id] = peerConnection;
  let stream = player.srcObject;
  stream.getTracks().forEach(track => peerConnection.addTrack(track, stream));
  peerConnection.onicecandidate = event => {
    if (event.candidate) {
      socket.emit('candidate', id, event.candidate);
    }
  };
  peerConnection
    .createOffer()
    .then(sdp => peerConnection.setLocalDescription(sdp))
    .then(() => {
      socket.emit('offer', id, peerConnection.localDescription);
    });
});
socket.on('answer', (id, description) => {
  peerConnections[id].setRemoteDescription(description);
});
socket.on('candidate', (id, candidate) => {
  peerConnections[id].addIceCandidate(new RTCIceCandidate(candidate));
});
socket.on('disconnectPeer', id => {
  delete peerConnections[id];
});
window.onunload = window.onbeforeunload = () => {
  socket.close();
}

navigator.mediaDevices.getUserMedia(constraints)
  .then((stream) => {
    // Play stream from webcam on screen
    player.srcObject = stream;
    // Initialise peer-to-peer connection
    socket.emit('broadcaster');
    // Initialise media recorder
    mediaRecorder = new MediaRecorder(stream, {
      mimeType: 'video/mp4',
    });
    let chunks = [];
    mediaRecorder.ondataavailable = function(e) {
      chunks.push(e.data);
    }
    // Register a handler when the media recorder stops to grab the blob and
    // upload it to the server
    mediaRecorder.onstop = function(e) {
      const blob = new Blob(chunks, {'type' : 'video/mp4'});
      // Clear the buffer
      chunks = [];
      let formData = new FormData();
      formData.append('video', blob);
      fetch('/upload', {
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
        })
    }
    // Start main loop
    update();
  });

// Default thresholds
var globalThreshold;
var pixelThreshold;
const waitTime = 2000;
const smoothing = 20;
const resolution = 100;
const clipLength = 3000;

// Controls
var  slider = document.getElementById('sensitivity');
slider.max = 100;
slider.min = 0;
slider.value = 50;
function thresholds(value) {
  let pixelThreshold = Math.abs(value - 100) * 0.5 + 20;
  let globalThreshold = Math.abs(value - 100) * 10;
  return [pixelThreshold, globalThreshold];
}
var [pixelThreshold, globalThreshold] = thresholds(slider.value);
slider.oninput = function() {
  [pixelThreshold, globalThreshold] = thresholds(this.value)
}
var captureImages = document.getElementById('captureImages');
var captureVideos = document.getElementById('captureVideos');

function motionDetect(){
  var motion = [];
  // Draw video onto the screen
  context.drawImage(player, 0, 0, canvas.width, canvas.height);
  var data = context.getImageData(0, 0, canvas.width, canvas.height).data;
  // Loop through the rows and columns
  for (var y=0; y<canvas.height; y += sampleSize) {
    for (var x=0; x<canvas.width; x += sampleSize) {
      // the data array is a continuous array of red, blue, green
      // and alpha values, so each pixel takes up four values
      // in the array
      var pos = (x + y * canvas.width) * 4;
      // get red, blue and green pixel value
      var r = data[pos];
      var g = data[pos+1];
      var b = data[pos+2];
      // draw the pixels as blocks of colours
      if(previousFrame[pos] && Math.abs(previousFrame[pos] - r) > pixelThreshold) {
        motion.push({x: x, y: y, r: r, g: g, b: b});
      }
    }
  }
  previousFrame = data;
  return motion;
}

// Movement on/off should be confirmed only if sustained for a certain period
var motionHistory = []
var globalMotion = 0;
var waiting = false;
// Array to hold pixel values of previous frame
var previousFrame = [];
// Sample the image every N pixels
var sampleSize =  Math.round(canvas.width / resolution);

function update() {
  // compare current frame to previous to detect changed pixels
  var motion = motionDetect();
  motionHistory.push(motion.length);
  if (motionHistory.length > smoothing) {
    motionHistory.shift()
  }
  // track sum of motion over recent frames
  globalMotion = motionHistory.reduce((a,b) => a+b);
  let alarm = document.getElementById('alarm');
  alarm.innerHTML = globalMotion;
  if (waiting) {
    // Wait before resetting the alarm
  } else if (globalMotion > globalThreshold) {
    // Motion alarm
    alarm.style.backgroundColor = 'red';
    waiting = true;
    // Capture video clip from media recorder
    if (captureVideos.checked && mediaRecorder.state === 'inactive') {
      mediaRecorder.start();
      console.log(`Starting media recorder... ${mediaRecorder.state}`);
      setTimeout(() => {
        mediaRecorder.stop();
        console.log(`Stopping media recorder... ${mediaRecorder.state}`);
      }, clipLength)
    }
    // Capture snapshot from canvas and upload to server
    if (captureImages.checked) {
      canvas.toBlob(function(blob) {
        let formData = new FormData();
        formData.append('image', blob);
        fetch('/upload', {
          method: 'POST',
          body: formData
        })
          .then(response => response.json())
          .then(data => {
            console.log(data);
          })
      }, "image/jpeg")
    }
    setTimeout(function () {
      waiting = false;
    }, waitTime)
  } else if (globalMotion > globalThreshold * 0.2) {
    // Warning
    alarm.style.backgroundColor = 'orange';
  } else {
    // No motion detected
    alarm.style.backgroundColor = 'white';
  }
  // Highlight motion on the video
  for (i=0; i< motion.length; i++) {
    var m = motion[i];
    context.fillStyle = 'green';
    context.fillRect(m.x, m.y, sampleSize, sampleSize);
  }
  setTimeout(update, 1000 / 60);
}
