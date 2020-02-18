var config = require('./config');
var ks = require('node-key-sender');
const Bot = require('node-telegram-bot-api');
const token = config.red_token;

const bot = new Bot(token, {polling: true});

bot.on('start', message=> {
  console.log(message);
  bot.sendMessage(message.chat.id, 'Hi ' + message.from.first_name + ' , send your first command to Pokemon Red!', {
    reply_markup: {
      keyboard: [["UP", 'DOWN', 'LEFT', 'RIGHT'], ['A','B','START','SELECT']]
    }
  });
});

bot.on('text', message=> {
  console.log(message);
  if(message.text.startsWith("/start")){
		bot.sendMessage(message.chat.id, 'Hi ' + message.from.first_name + ', send your first command to Pokemon Red!', {
		reply_markup: {
		  keyboard: [["UP", 'DOWN', 'LEFT', 'RIGHT'], ['A','B','START','SELECT']]
		}
	  });
  }else{
	  
	  var command = message.text;
	  
	  switch(command){
		  case "UP":
			ks.sendKey(config.red.UP);
			//message.reply("UP command sent");
			break;
		  case "DOWN":
			ks.sendKey(config.red.DOWN);
			//message.reply("DOWN command sent");
			break;
		  case "LEFT":
			ks.sendKey(config.red.LEFT);
			//message.reply("LEFT command sent");
			break;
		  case "RIGHT":
			ks.sendKey(config.red.RIGHT);
			//message.reply("RIGHT command sent");
			break;
		  case "A":
			ks.sendKey(config.red.A);
			//message.reply("A command sent");
			break;
		  case "B":
			ks.sendKey(config.red.B);
			//message.reply("B command sent");
			break;
		  case "START":
			ks.sendKey(config.red.START);
			//message.reply("START command sent");
			break;
		  case "SELECT":
			ks.sendKey(config.red.SELECT);
			//message.reply("SELECT command sent");
			break;
	  }
	  
	  bot.sendMessage(message.chat.id, 'Send the next command!', {
		reply_markup: {
		  keyboard: [["UP", 'DOWN', 'LEFT', 'RIGHT'], ['A','B','START','SELECT']]
		}
	  });
  }
});