const Telegraf = require('telegraf');
const bot = new Telegraf("913448919:AAFkldBhryyiMHbrNbSF_r06Jl4fC0kIjbI");
bot.start((message) => {
  console.log('started:', message.from.id)
  return message.reply('Hello my friend, contact me by send /contact, or write anything');
})
bot.on('text', message=> {
  const subreddit = message.message.text;
  return message.reply("Ciao, mi hai scritto " + message.message.text);
});
bot.startPolling();