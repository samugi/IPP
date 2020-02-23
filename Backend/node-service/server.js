const express = require('express');
var ks = require('node-key-sender');
ks.setOption('globalDelayPressMillisec', 150);
const app = express();

var io = require('socket.io-client')
var socket = io.connect('http://localhost:3000', {reconnect: true});
var raidReady = false;

var bm = ;
var raidWinner;
var duration;
var bmStartedTs;

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
    res.json({bm:bm, raidWinner:raidWinner, bmStartedTs:bmStartedTs, duration:duration});
});

app.get('/send-bm', (req, res) => {
    console.log(`Request coming from IP: ` + req.connection.remoteAddress);
    bm = req.query.bm;
    raidWinner = req.query.w;
    duration = req.query.d;
    bmStartedTs = req.query.ts;
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
