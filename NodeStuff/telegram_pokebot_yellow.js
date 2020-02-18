var config = require('./config');
var ks = require('node-key-sender');
const Bot = require('node-telegram-bot-api');
const token = config.yellow_token;

const bot = new Bot(token, {polling: true});

bot.on('start', message=> {
  console.log(message);
  bot.sendMessage(message.chat.id, 'Hi ' + message.from.first_name + ' , send your first command to Pokemon Yellow!', {
    reply_markup: {
      keyboard: [["UP", 'DOWN', 'LEFT', 'RIGHT'], ['A','B','START','SELECT']]
    }
  });
});

bot.on('text', message=> {
  console.log(message);
  if(message.text.startsWith("/start")){
		bot.sendMessage(message.chat.id, 'Hi ' + message.from.first_name + ', send your first command to Pokemon Yellow!', {
		reply_markup: {
		  keyboard: [["UP", 'DOWN', 'LEFT', 'RIGHT'], ['A','B','START','SELECT']]
		}
	  });
  }else{
	  
	  var command = message.text;
	  
	  switch(command){
		  case "UP":
			ks.sendKey(config.yellow.UP);
			//message.reply("UP command sent");
			break;
		  case "DOWN":
			ks.sendKey(config.yellow.DOWN);
			//message.reply("DOWN command sent");
			break;
		  case "LEFT":
			ks.sendKey(config.yellow.LEFT);
			//message.reply("LEFT command sent");
			break;
		  case "RIGHT":
			ks.sendKey(config.yellow.RIGHT);
			//message.reply("RIGHT command sent");
			break;
		  case "A":
			ks.sendKey(config.yellow.A);
			//message.reply("A command sent");
			break;
		  case "B":
			ks.sendKey(config.yellow.B);
			//message.reply("B command sent");
			break;
		  case "START":
			ks.sendKey(config.yellow.START);
			//message.reply("START command sent");
			break;
		  case "SELECT":
			ks.sendKey(config.yellow.SELECT);
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