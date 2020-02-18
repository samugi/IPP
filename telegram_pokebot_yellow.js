const Telegraf = require('telegraf');
const bot = new Telegraf("1009680526:AAEsuM2QVJ4crjSB5T1Y4Dp8YMU0DfGM_XM");
bot.start((message) => {
  console.log('started:', message.from.id)
  return message.reply('Hello my friend, contact me by send /contact, or write anything');
})
bot.on('text', message=> {
  const subreddit = message.message.text;
  return message.reply("Ciao, mi hai scritto " + message.message.text);
});
bot.startPolling();