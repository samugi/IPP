const Mixer = require('@mixer/client-node');
var config = require('./config');
var ks = require('node-key-sender');
const ws = require('ws');
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
const SOURCE = 'MIXER';

let userInfo;

const client = new Mixer.Client(new Mixer.DefaultRequestRunner());

// With OAuth we don't need to log in. The OAuth Provider will attach
// the required information to all of our requests after this call.
client.use(new Mixer.OAuthProvider(client, {
	tokens: {
		access:  '6EKgPgzoZl5cjBiSpfnwgPj21TWf2UPGHuXZoHWg4VsdSTvaBVxp5ojhlmtfLNtg',
		expires: Date.now() + (365 * 24 * 60 * 60 * 1000)
	},
}));

// Gets the user that the Access Token we provided above belongs to.
client.request('GET', 'users/current')
.then(response => {
	console.log(response.body);

	// Store the logged in user's details for later reference
	userInfo = response.body;

	// Returns a promise that resolves with our chat connection details.
	return new Mixer.ChatService(client).join(response.body.channel.id);
})
.then(response => {
	const body = response.body;
	console.log(body);
	return createChatSocket(userInfo.id, userInfo.channel.id, body.endpoints, body.authkey);
})
.catch(error => {
	console.error('Something went wrong.');
	console.error(error);
});


function sendCommand(socket, user, command, pkmnVersion){
	socket.call('msg', [ user + ' Sending '+command+' command to pokemon '+pkmnVersion+'!']);
	console.log(command + ' ' + pkmnVersion);
	var options = SOURCE + ' ' + user + ' '+ command + ' ' + pkmnVersion;
}

/**
    * Creates a Mixer chat socket and sets up listeners to various chat events.
    * @param {number} userId The user to authenticate as
    * @param {number} channelId The channel id to join
    * @param {string[]} endpoints An array of endpoints to connect to
    * @param {string} authkey An authentication key to connect with
    * @returns {Promise.<>}
    */
function createChatSocket (userId, channelId, endpoints, authkey) {
        // Chat connection
        const socket = new Mixer.Socket(ws, endpoints).boot();

        // Greet a joined user
        socket.on('UserJoin', data => {
            socket.call('msg', [`Hi ${data.username}! I'm pokèbot! You can control all of the pokèmon version streamed! How? Send one of this command: !up, !down, !left, !right, !a, !b, !start or !select followed by the pokèmon version! For example: !up blue`]);
        });

        // React to our !pong command
        socket.on('ChatMessage', data => {
			var message = data.message.message[0].data.toLowerCase().split(' ');
			var user = data.user_name;
			if(message.length == 2){
				if (message[0] == '!up') { //UP
					if (message[1].toLowerCase().startsWith('blue')){
						ks.sendKey(config.blue.UP);
						sendCommand(socket, user, UP, BLUE);
					}else if (message[1].startsWith('red')){
						ks.sendKey(config.red.UP);
						sendCommand(socket, user, UP, RED);
					}else if (message[1].startsWith('yellow')){
						ks.sendKey(config.yellow.UP);
						sendCommand(socket, user, UP, YELLOW);
					}
					
				}else if (message[0] == '!down') { //DOWN
					if (message[1].startsWith('blue')){
						ks.sendKey(config.blue.DOWN);
						sendCommand(socket, user, DOWN, BLUE);
					}else if (message[1].startsWith('red')){
						ks.sendKey(config.red.DOWN);
						sendCommand(socket, user, DOWN, RED);
					}else if (message[1].startsWith('yellow')){
						ks.sendKey(config.yellow.DOWN);
						sendCommand(socket, user, DOWN, YELLOW);
					}
				}else if (message[0] == '!left') { //LEFT
					if (message[1].startsWith('blue')){
						ks.sendKey(config.blue.LEFT);
						sendCommand(socket, user, LEFT, BLUE);
					}else if (message[1].startsWith('red')){
						ks.sendKey(config.red.LEFT);
						sendCommand(socket, user, LEFT, RED);
					}else if (message[1].startsWith('yellow')){
						ks.sendKey(config.yellow.LEFT);
						sendCommand(socket, user, LEFT, YELLOW);
					}
				}else if (message[0] == '!right') { //RIGHT
					if (message[1].startsWith('blue')){
						ks.sendKey(config.blue.RIGHT);
						sendCommand(socket, user, RIGHT, BLUE);
					}else if (message[1].startsWith('red')){
						ks.sendKey(config.red.RIGHT);
						sendCommand(socket, user, RIGHT, RED);
					}else if (message[1].startsWith('yellow')){
						ks.sendKey(config.yellow.RIGHT);
						sendCommand(socket, user, RIGHT, YELLOW);
					}
				}else if (message[0] == '!a') { //A
					if (message[1].startsWith('blue')){
						ks.sendKey(config.blue.A);
						sendCommand(socket, user, A, BLUE);
					}else if (message[1].startsWith('red')){
						ks.sendKey(config.red.A);
						sendCommand(socket, user, A, RED);
					}else if (message[1].startsWith('yellow')){
						ks.sendKey(config.yellow.A);
						sendCommand(socket, user, A, YELLOW);
					}
				}else if (message[0] == '!b') { //B
					if (message[1].startsWith('blue')){
						ks.sendKey(config.blue.B);
						sendCommand(socket, user, B, BLUE);
					}else if (message[1].startsWith('red')){
						ks.sendKey(config.red.B);
						sendCommand(socket, user, B, RED);
					}else if (message[1].startsWith('yellow')){
						ks.sendKey(config.yellow.B);
						sendCommand(socket, user, B, YELLOW);
					}
				}else if (message[0] == '!start') { //START
					if (message[1].startsWith('blue')){
						ks.sendKey(config.blue.START);
						sendCommand(socket, user, START, BLUE);
					}else if (message[1].startsWith('red')){
						ks.sendKey(config.red.START);
						sendCommand(socket, user, START, RED);
					}else if (message[1].startsWith('yellow')){
						ks.sendKey(config.yellow.START);
						sendCommand(socket, user, START, YELLOW);
					}
				}else if (message[0] == '!select') { //SELECT
					if (message[1].startsWith('blue')){
						ks.sendKey(config.blue.SELECT);
						sendCommand(socket, user, SELECT, BLUE);
					}else if (message[1].startsWith('red')){
						ks.sendKey(config.red.SELECT);
						sendCommand(socket, user, SELECT, RED);
					}else if (message[1].startsWith('yellow')){
						ks.sendKey(config.yellow.SELECT);
						sendCommand(socket, user, SELECT, YELLOW);
					}
				}
			}
        });

        // Handle errors
        socket.on('error', error => {
            console.error('Socket error');
            console.error(error);
        });

        return socket.auth(channelId, userId, authkey)
        .then(() => {
            console.log('Login successful');
            return socket.call('msg', [`Hi I'm pokèbot! You can control all of the pokèmon version streamed! How? Send one of this command: !up, !down, !left, !right, !a, !b, !start or !select followed by the pokèmon version! For example: !up blue`]);
        });
    }