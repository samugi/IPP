var config = require('./config');
var ks = require('node-key-sender');
const Bot = require('node-telegram-bot-api');
const token = config.blue_token;

const bot = new Bot(token, {polling: true});

bot.on('start', message=> {
  console.log(message);
  bot.sendMessage(message.chat.id, 'Hi ' + message.from.first_name + ' , send your first command to Pokemon Blue!', {
    reply_markup: {
      keyboard: [["UP", 'DOWN', 'LEFT', 'RIGHT'], ['A','B','START','SELECT']]
    }
  });
});

bot.on('text', message=> {
  console.log(message);
  if(message.text.startsWith("/start")){
		bot.sendMessage(message.chat.id, 'Hi ' + message.from.first_name + ', send your first command to Pokemon Blue!', {
		reply_markup: {
		  keyboard: [["UP", 'DOWN', 'LEFT', 'RIGHT'], ['A','B','START','SELECT']]
		}
	  });
  }else{
	  
	  var command = message.text;
	  
	  switch(command){
		  case "UP":
			ks.sendKey(config.blue.UP);
			//message.reply("UP command sent");
			break;
		  case "DOWN":
			ks.sendKey(config.blue.DOWN);
			//message.reply("DOWN command sent");
			break;
		  case "LEFT":
			ks.sendKey(config.blue.LEFT);
			//message.reply("LEFT command sent");
			break;
		  case "RIGHT":
			ks.sendKey(config.blue.RIGHT);
			//message.reply("RIGHT command sent");
			break;
		  case "A":
			ks.sendKey(config.blue.A);
			//message.reply("A command sent");
			break;
		  case "B":
			ks.sendKey(config.blue.B);
			//message.reply("B command sent");
			break;
		  case "START":
			ks.sendKey(config.blue.START);
			//message.reply("START command sent");
			break;
		  case "SELECT":
			ks.sendKey(config.blue.SELECT);
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