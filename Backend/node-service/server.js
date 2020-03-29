const express = require('express');
var ks = require('node-key-sender');
ks.setOption('globalDelayPressMillisec', 150);
const app = express();
var fs = require('fs');
var http = require('http')
var https = require('https')
var Queue = require('better-queue');
var privateKey  = fs.readFileSync('sslcert/server.key', 'utf8');
var certificate = fs.readFileSync('sslcert/server.crt', 'utf8');
var credentials = {key: privateKey, cert: certificate};
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
const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://mizane:R4izarulez@clusteripp-qugaa.gcp.mongodb.net/test?retryWrites=true&w=majority";


MongoClient.connect(uri, function (err, clientMongo) {
		try {
			if (err) throw err;
			dbMongoVolante = clientMongo.db('test');
		}catch(err){
		}
	}
);


var twitchCommandsQueue = new Queue(function (command, cb) {
	console.log("Command: " + command.command + ", platform: " + command.platform + ", user: " + command.user + ", buttonPressed:" + command.joyPad);
  ks.sendKey(command.joyPad);
  socket.emit('new_command_yellow',{command: command.command, username: command.user})
  twitchQueueSize--;
	cb();
}, {afterProcessDelay: 150});
var mixerCommandsQueue = new Queue(function (command, cb) {
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
    if(platform == 'twitch' || platform == 'app-twitch'){
	  var platformQueue = 'twitch';
      if(twitchQueueSize < queueSizeLimit){
        twitchCommandsQueue.push({command:command, platform:platformQueue, user:user, joyPad:joyPad});
        twitchQueueSize++;
      }else{
        console.log("adesso lo scarto perche e lungo " + twitchQueueSize)
      }
    }else if(platform == 'mixer' || platform == 'app-mixer'){
	  var platformQueue = 'mixer';
      if(mixerQueueSize < queueSizeLimit){
        mixerCommandsQueue.push({command:command, platform:platformQueue, user:user, joyPad:joyPad});
        mixerQueueSize++;
      }else{
        console.log("adesso lo scarto perche e lungo " + mixerQueueSize)
      }
    }else if(platform == 'youtube' || platform == 'app-youtube'){
	  var platformQueue = 'youtube';
      if(youtubeQueueSize < queueSizeLimit){
        youtubeCommandsQueue.push({command:command, platform:platformQueue, user:user, joyPad:joyPad});
        youtubeQueueSize++;
      }else{
        console.log("adesso lo scarto perche e lungo " + youtubeQueueSize)
      }
    }
	
	logCommandToDb(user, platform, command);
	
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
/*const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});*/

var httpServer = http.createServer(app);
var httpsServer = https.createServer(credentials, app);
httpServer.listen(8080);
httpsServer.listen(8443);

function logCommandToDb(username, platform, command){
	try{
		dbMongoVolante.collection('LOG_COMMAND').insertOne({"username": username, "platform": platform, "command": command, "timestamp": new Date().getTime()}, function (findErr, result) {
			if (findErr) throw findErr;
			if(logLevel >= DEBUG){
				console.log("log_command result:" + result);
			}
			if(logLevel >= TRACE){
				console.log("stored command in db: username: " + username +", platform: "+ platform +", command: "+ command);
			}
		});
	}catch(err){
		if(logLevel >= ERROR){
			console.log(err + " e ghe sboro");
		}
	}
}
