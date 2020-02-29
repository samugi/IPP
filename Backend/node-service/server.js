const express = require('express');
var ks = require('node-key-sender');
ks.setOption('globalDelayPressMillisec', 150);
const app = express();
var Queue = require('better-queue');

var io = require('socket.io-client')
var socket = io.connect('http://localhost:3000', {reconnect: true});
var raidReady = false;

var bm = "none";
var raidWinner = "none";
var duration = 0;
var bmStartedTs = 0;

var twitchQueueSize = 0;
var mixerQueueSize = 0
var youtubeQueueSize = 0;
var queueSizeLimit = 100;

var twitchCommandsQueue = new Queue(function (command, cb) {
	console.log("Command: " + command.command + ", platform: " + command.platform + ", user: " + command.user + ", buttonPressed:" + command.joyPad);
  ks.sendKey(command.joyPad);
  socket.emit('new_command_yellow',{command: command.command, username: command.user})
  twitchQueueSize--;
	cb();
}, {afterProcessDelay: 150});
var mixerCommandsQueue = new Queue(function (command, cb) {
  mixerQueueSize++;
	console.log("Command: " + command.command + ", platform: " + command.platform + ", user: " + command.user + ", buttonPressed:" + command.joyPad);
  ks.sendKey(command.joyPad);
  socket.emit('new_command_blue',{command: command.command, username: command.user})
  mixerQueueSize--;
	cb();
}, {afterProcessDelay: 150});
var youtubeCommandsQueue = new Queue(function (command, cb) {
	console.log("Command: " + command.command + ", platform: " + command.platform + ", user: " + command.user + ", buttonPressed:" + command.joyPad);
  ks.sendKey(command.joyPad);
  socket.emit('new_command_red',{command: command.command, username: command.user})
  youtubeQueueSize--;
	cb();
}, {afterProcessDelay: 150});


app.get('/send-command', (req, res) => {
    console.log(`Request coming from IP: ` + req.connection.remoteAddress);
    var command = req.query.command;
    var platform = req.query.platform;
    var user = req.query.user;
    var joyPad = req.query.joycommand
	
    //ks.sendKey(joyPad);
    if(platform == 'twitch'){
      if(twitchQueueSize < queueSizeLimit){
        twitchCommandsQueue.push({command:command, platform:platform, user:user, joyPad:joyPad});
        twitchQueueSize++;
      }else{
        console.log("adesso lo scarto perche e lungo " + twitchQueueSize)
      }
    }else if(platform == 'mixer'){
      if(mixerQueueSize < queueSizeLimit){
        mixerCommandsQueue.push({command:command, platform:platform, user:user, joyPad:joyPad});
        mixerQueueSize++;
      }else{
        console.log("adesso lo scarto perche e lungo " + mixerQueueSize)
      }
    }else if(platform == 'youtube'){
      if(youtubeQueueSize < queueSizeLimit){
        youtubeCommandsQueue.push({command:command, platform:platform, user:user, joyPad:joyPad});
        youtubeQueueSize++;
      }else{
        console.log("adesso lo scarto perche e lungo " + youtubeQueueSize)
      }
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
	socket.emit('send_bm',{raidWinner: raidWinner, duration:duration, bm:bm})
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
