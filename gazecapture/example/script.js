// Create a connection to the Runway HTTP Server
// You should select HTTP from the INPUT Panel
// *You should update this address to match the URL provided by the app
var socket = io.connect('http://127.0.0.1:33000/query');

// Wait until the page is loaded
document.addEventListener("DOMContentLoaded", function(event) {
  // Get the DOM elements
  var status = document.getElementById('status');
  var log = document.getElementById('log');
  var startBtn = document.getElementById('start');
  var stopBtn = document.getElementById('stop');
  var video = document.querySelector('video');
  var canvas = document.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var localMediaStream = null;
  var shouldLoop = false;

  // Get the user's camera
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        video.src = window.URL.createObjectURL(stream);
        video.play();
      });
  }

  // When a connection is established
  socket.on('connect', function() {
    status.innerHTML = 'Connected';
  });

  // When there is new data coming in, update the log element
  socket.on('update_response', function(data) {
    console.log(data.results);
    if (shouldLoop) {
      sendImage();
    }
  });

  // Get the current frame and send it to Runway using the Canvas API
  function sendImage() {
    ctx.drawImage(video, 0, 0, 300, 280);
    // Send to Runway the current element in the canvas
    socket.emit('update_request', {
      data: canvas.toDataURL('image/jpeg')
    });
  }

  // Start the loop: send an image, wait for response, send another one...
  function start() {
    shouldLoop = true;
    sendImage()
  }

  // Stop the loop
  function stop() {
    shouldLoop = false;
  }

  // Listen to start and stop event
  startBtn.addEventListener('click', start, false);
  stopBtn.addEventListener('click', stop, false);
});