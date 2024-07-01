/*
Discord module.
*/
import { Client, IntentsBitField } from 'discord.js';
import dotenv from 'dotenv';
dotenv.config()
// Import module
import {main} from "./utils/main_function.js"
import {logoutGmail} from "./utils/helper_functions.js"
// Create Client Instance
const client = new Client({
  intents: [
    IntentsBitField.Flags.Guilds,
    IntentsBitField.Flags.GuildMessages,
    IntentsBitField.Flags.MessageContent,
  ],
});

// Display message when bot is ready
client.on('ready', () => {
  console.log('The bot is online!');
});

// Trigger on new message
client.on('messageCreate', async (message) => {
    if (message.author.bot) return;
    if (message.channel.id !== process.env.CHANNEL_ID) return;
    if (message.content.startsWith('!')) return;
  
    // Send typing indicator initially
    await message.channel.sendTyping();


    let conversationLog = [];
  
    try {
      let prevMessages = await message.channel.messages.fetch({ limit: 15 });
      prevMessages.reverse();
      
      // Send typing indicator before processing each message
      await message.channel.sendTyping();

      // loop over each message 
      prevMessages.forEach((msg) => {
        if (msg.content.startsWith('!')) return;
        if (msg.author.id !== client.user.id && message.author.bot) return;
        if (msg.author.id == client.user.id) {
          conversationLog.push({
            role: 'assistant',
            content: msg.content,
            name: msg.author.username
              .replace(/\s+/g, '_')
              .replace(/[^\w\s]/gi, ''),
          });
        }
  
        if (msg.author.id == message.author.id) {
          conversationLog.push({
            role: 'user',
            content: msg.content,
            name: message.author.username
              .replace(/\s+/g, '_')
              .replace(/[^\w\s]/gi, ''),
          });
        }
      });

      console.log(conversationLog)
      // Calling main function
      const [result, page, login_status, browser] = await main(message.content);
      message.reply(result);

      // Logout google account
      if(login_status){
        console.log("logout from Google account")

        // Call the logout function
        const logout_reponse = await logoutGmail(page);
        if (logout_reponse) {
            console.log("Successfully logged out.");
            
            // close the browser
            await browser.close();
        } else {
            console.log("Failed to log out.");
        }
    }
    } catch (error) {
      console.log(`ERR: ${error}`);
    }
  });
client.login(process.env.TOKEN);
