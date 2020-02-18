const Telegraf = require('telegraf');
const bot = new Telegraf("973106231:AAFB6B6j5Foe5COAnFXau5cpJvVGvxrR_H0");
bot.start((message) => {
  console.log('started:', message.from.id)
  return message.reply('Hello my friend, contact me by send /contact, or write anything');
})
bot.on('text', message=> {
  const subreddit = message.message.text;
  return message.reply("Ciao, mi hai scritto " + message.message.text);
});
bot.startPolling();