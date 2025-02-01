dotenv.config();
import { Client, IntentsBitField } from "discord.js";
import dotenv from "dotenv";
import OpenAI from "openai";
import { loginGoogle_navigateToGmail } from "./components/puppeteer/login_automation.js";
import { fetchEmailsAndAttachments } from "./components/puppeteer/automation_response.js";
import { logoutGmail } from "./components/puppeteer/puppeteer_automation_helper.js";

// Create OpenAI object
const openai = new OpenAI({ apiKey: process.env.API_KEY });

// Create Client Instance
const client = new Client({
  intents: [
    IntentsBitField.Flags.Guilds,
    IntentsBitField.Flags.GuildMessages,
    IntentsBitField.Flags.MessageContent,
  ],
});

// Intialize variables
let isLoggedIn = false;
let result = "";
let page = null;
let browser = null;

// Display message when bot is ready
client.on("ready", () => {
  console.log("The bot is online!");
});

// Trigger on new message
client.on("messageCreate", async (message) => {
  // Prevent bot from reacting to it's own messages
  if (message.author.bot) return;

  // Only allow 1 Channel (will change in Production)
  if (message.channel.id !== process.env.CHANNEL_ID) return;

  // Show typing indicator
  const sendTypingInterval = setInterval(() => {
    message.channel.sendTyping();
  }, 4000);

  try {
    // Fetch last 15 history messages
    let historyMessages = await message.channel.messages.fetch({ limit: 15 });
    historyMessages.reverse();

    // Create formatted History Output
    let historyOutput = [];
    historyMessages.forEach((historyMessage) => {
      if (historyMessage.author.id !== client.user.id && message.author.bot)
        return;

      // Check if Message-Author is the Bot
      if (historyMessage.author.id == client.user.id) {
        historyOutput.push({
          role: "assistant",
          content: historyMessage.content,
          name: historyMessage.author.username
            .replace(/\s+/g, "_")
            .replace(/[^\w\s]/gi, ""),
        });
      }

      // Check if Message-Author is User who Sent the Original Message
      if (historyMessage.author.id == message.author.id) {
        historyOutput.push({
          role: "user",
          content: historyMessage.content,
          name: message.author.username
            .replace(/\s+/g, "_")
            .replace(/[^\w\s]/gi, ""),
        });
      }
    });

    // Trim message.content
    const content = message.content.trim();

    // "!history"-Message
    if (content.startsWith("!history")) {
      const userQuery = content.slice("!history".length).trim();
      const result = await openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: historyOutput,
        max_tokens: 2000, // limit token usage
      });
      message.reply(result.choices[0].message.content);
    }

    // "!logout"-Message
    else if (content.startsWith("!logout")) {
      // Logout google account
      if (isLoggedIn) {
        console.log("logout from Google account");

        // Call logout function
        const logout_reponse = await logoutGmail(page);

        // Check logout response true or false
        if (logout_reponse) {
          message.reply("Successfully logged out.");

          // Close browser
          await browser.close();
        } else {
          message.reply("Failed to log out.");
        }
      }
    } else {
      // All other Messages
      if (isLoggedIn) {
        //TODO THIS NEVER HAPPENS
        [result, page, isLoggedIn, browser] = await fetchEmailsAndAttachments(
          message.content + " Action:email",
          page,
          browser
        );
      } else {
        [result, page, isLoggedIn, browser] = await loginGoogle_navigateToGmail(
          message.content + " Action:email"
        );
      }
      message.reply(result);
    }

    // Clear Typing-Interval
    clearInterval(sendTypingInterval);
  } catch (error) {
    console.log(`ERR: ${error}`);
  }
});
client.login(process.env.DISCORD_TOKEN);
