const tmi = require('tmi.js');
var config = require('./config');
var ks = require('node-key-sender');

const UP = 'UP';
const DOWN = 'DOWN';
const LEFT = 'LEFT';
const RIGHT = 'RIGHT';
const A = 'A';
const B = 'B';
const START = 'START';
const SELECT = 'SELECT';
const RED = 'Red';
const BLUE = 'Blue';
const YELLOW = 'Yellow';
const SOURCE = 'TWITCH';

// Define configuration options
const opts = {
  identity: {
    username: config.twitch_username,
    password: config.twitch_oauth
  },
  channels: [
    config.twitch_channel
  ]
};
// Create a client with our options
const client = new tmi.client(opts);

// Register our event handlers (defined below)
client.on('message', onMessageHandler);
client.on('connected', onConnectedHandler);

// Connect to Twitch:
client.connect();

// Called every time a message comes in
function onMessageHandler (target, context, msg, self) {
  if (self) { return; } // Ignore messages from the bot

	var message = msg.toLowerCase().split(' ');
	if(message.length == 2){
		if (message[0] == '!up') { //UP
			if (message[1].toLowerCase().startsWith('blue')){
				sendCommand(client, target, UP, BLUE);
				ks.sendKey(config.blue.UP);
			}else if (message[1].startsWith('red')){
				sendCommand(client, target, UP, RED);
				ks.sendKey(config.red.UP);
			}else if (message[1].startsWith('yellow')){
				sendCommand(client, target, UP, YELLOW);
				ks.sendKey(config.yellow.UP);
			}
			
		}else if (message[0] == '!down') { //DOWN
			if (message[1].startsWith('blue')){
				sendCommand(client, target, DOWN, BLUE);
				ks.sendKey(config.blue.DOWN);
			}else if (message[1].startsWith('red')){
				ks.sendKey(config.red.DOWN);
				sendCommand(client, target, DOWN, RED);
			}else if (message[1].startsWith('yellow')){
				ks.sendKey(config.yellow.DOWN);
				sendCommand(client, target, DOWN, YELLOW);
			}
		}else if (message[0] == '!left') { //LEFT
			if (message[1].startsWith('blue')){
				ks.sendKey(config.blue.LEFT);
				sendCommand(client, target, LEFT, BLUE);
			}else if (message[1].startsWith('red')){
				ks.sendKey(config.red.LEFT);
				sendCommand(client, target, LEFT, RED);
			}else if (message[1].startsWith('yellow')){
				ks.sendKey(config.yellow.LEFT);
				sendCommand(client, target, LEFT, YELLOW);
			}
		}else if (message[0] == '!right') { //RIGHT
			if (message[1].startsWith('blue')){
				ks.sendKey(config.blue.RIGHT);
				sendCommand(client, target, RIGHT, BLUE);
			}else if (message[1].startsWith('red')){
				ks.sendKey(config.red.RIGHT);
				sendCommand(client, target, RIGHT, RED);
			}else if (message[1].startsWith('yellow')){
				ks.sendKey(config.yellow.RIGHT);
				sendCommand(client, target, RIGHT, YELLOW);
			}
		}else if (message[0] == '!a') { //A
			if (message[1].startsWith('blue')){
				ks.sendKey(config.blue.A);
				sendCommand(client, target, A, BLUE);
			}else if (message[1].startsWith('red')){
				ks.sendKey(config.red.A);
				sendCommand(client, target, A, RED);
			}else if (message[1].startsWith('yellow')){
				ks.sendKey(config.yellow.A);
				sendCommand(client, target, A, YELLOW);
			}
		}else if (message[0] == '!b') { //B
			if (message[1].startsWith('blue')){
				ks.sendKey(config.blue.B);
				sendCommand(client, target, B, BLUE);
			}else if (message[1].startsWith('red')){
				ks.sendKey(config.red.B);
				sendCommand(client, target, B, RED);
			}else if (message[1].startsWith('yellow')){
				ks.sendKey(config.yellow.B);
				sendCommand(client, target, B, YELLOW);
			}
		}else if (message[0] == '!start') { //START
			if (message[1].startsWith('blue')){
				ks.sendKey(config.blue.START);
				sendCommand(client, target, START, BLUE);
			}else if (message[1].startsWith('red')){
				ks.sendKey(config.red.START);
				sendCommand(client, target, START, RED);
			}else if (message[1].startsWith('yellow')){
				ks.sendKey(config.yellow.START);
				sendCommand(client, target, START, YELLOW);
			}
		}else if (message[0] == '!select') { //SELECT
			if (message[1].startsWith('blue')){
				ks.sendKey(config.blue.SELECT);
				sendCommand(client, target, SELECT, BLUE);
			}else if (message[1].startsWith('red')){
				ks.sendKey(config.red.SELECT);
				sendCommand(client, target, SELECT, RED);
			}else if (message[1].startsWith('yellow')){
				ks.sendKey(config.yellow.SELECT);
				sendCommand(client, target, SELECT, YELLOW);
			}
		}
	}

}
// Function called when the "dice" command is issued
function rollDice () {
  const sides = 6;
  return Math.floor(Math.random() * sides) + 1;
}
function sendCommand(client, target, command, pkmnVersion){
	client.say(target, 'You have sent '+command+' command to pokemon '+pkmnVersion+'!');
    console.log(`* Executed ${command} command`);
	var options = SOURCE + ' ' + target.replace('#','') + ' '+ command + ' ' + pkmnVersion;
	
//	PythonShell.run('send_command.py', options , function (err, results) { 
//		console.log(err);
//	});
}
// Called every time the bot connects to Twitch chat
function onConnectedHandler (addr, port) {
  console.log(`* Connected to ${addr}:${port}`);
}