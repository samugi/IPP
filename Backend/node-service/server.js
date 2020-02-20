const express = require('express');
var ks = require('node-key-sender');
ks.setOption('globalDelayPressMillisec', 150);
const app = express();

var io = require('socket.io-client')
var socket = io.connect('http://localhost:3000', {reconnect: true});
var raidReady = false;

app.get('/send-command', (req, res) => {
  
    console.log(`Request coming from IP: ` + req.connection.remoteAddress);
    var command = req.query.command;
    var platform = req.query.platform;
    var user = req.query.user;
    var joyPad = req.query.joycommand
    ks.sendKey(joyPad);
    if(platform == 'mixer'){
      socket.emit('new_command_blue',{command: command, username: user})
    }else if(platform == 'twitch'){
      socket.emit('new_command_yellow',{command: command, username: user})
    }else if(platform == 'youtube'){
      socket.emit('new_command_red',{command: command, username: user})
    }
    console.log("Button: " + command + ", platform: " + platform + ", user: " + user);
    res.send('OK');
    
});

app.get('/raid', (req, res) => {
  
    res.send(raidReady);
	raidReady = false;
    
});

app.get('/setraid', (req, res) => {
  
  raidReady = true;
  res.send('OK');
    
});

// Listen to the App Engine-specified port, or 8080 otherwise
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});
