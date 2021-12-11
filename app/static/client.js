var socket = io();

socket.on('connect', () => {
  console.log('SocketIO connected!');
  socket.send('Hello, World!')
})

socket.on('message', (msg) => {
  console.log(msg)
});
