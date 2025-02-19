import StealthPlugin from "puppeteer-extra-plugin-stealth";
import puppeteer from "puppeteer-extra";
import OpenAI from "openai";
import dotenv from "dotenv";
import {
  imageToBase64,
  sleep,
  highlightLinks,
  waitForEvent,
  readPromptFromFile,
} from "./helper.js";
import {
  handleEmailNavigation,
  handleAttachmentDownload,
  processGPTResponse,
} from "./automation_response_helper.js";
dotenv.config();

const stealth = StealthPlugin(); // Pupeteer stealth configuration
stealth.enabledEvasions.delete("iframe.contentWindow");
stealth.enabledEvasions.delete("media.codecs");
puppeteer.use(stealth);

const folderPath = "./data";
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const timeout = 8000;

export async function fetchEmailsAndAttachments(
  userInput,
  web_page,
  web_browser
) {
  const browser = web_browser;
  const page = web_page;

  // Set viewport
  await page.setViewport({
    width: 1200,
    height: 1200,
    deviceScaleFactor: 1.75,
  });

  const main_prompt = await readPromptFromFile(
    "./components/puppeteer/prompts/openai_prompt.txt"
  );
  const messages = [
    { role: "system", content: main_prompt },
    { role: "user", content: userInput },
  ];

  // Initialize state variables
  let screenshot_taken = false;
  let openai_final_response = "";
  let action = "";
  let unread_email = false;
  let download_attachement_file = false;

  // Extract action from user input
  if (userInput.toLowerCase()) {
    const actionMatch = userInput.match(/Action:(\S+)/);
    action = actionMatch ? actionMatch[1] : "";
  }

  while (true) {
    if (page) {
      try {
        // Navigate to Gmail
        await page.goto("https://mail.google.com/mail/");
        await page.waitForNavigation({ waitUntil: "networkidle2" });

        await highlightLinks(page);
        await page.screenshot({ path: "screenshot_emails.jpg", quality: 100 });

        // Handle email navigation if action is specified
        if (action) {
          [unread_email, download_attachement_file, openai_final_response] =
            await handleEmailNavigation(page);

          if (openai_final_response === "No Unread email found") {
            break;
          }

          // Handle attachment download if email is found
          if (unread_email) {
            download_attachement_file = await handleAttachmentDownload(page);
          }
        }

        // Take screenshot of current state
        await highlightLinks(page);
        await Promise.race([waitForEvent(page, "load"), sleep(timeout)]);
        await page.screenshot({ path: "screenshot.jpg", quality: 100 });
        screenshot_taken = true;
      } catch (error) {
        console.error("Error during operation:", error);
      }
    }

    // Process response based on email state
    if (unread_email) {
      const response = await processGPTResponse(
        messages,
        openai,
        download_attachement_file,
        folderPath
      );
      return [response, page, browser];
    }
    // Handle screenshot-based navigation
    else if (screenshot_taken) {
      const base64_image = await imageToBase64("screenshot.jpg");
      messages.push({
        role: "user",
        content: [
          {
            type: "image_url",
            image_url: { url: base64_image },
          },
          {
            type: "text",
            text: 'Here\'s the screenshot of the website you are on right now. You can click on links with {"click": "Link text"} or you can crawl to another URL if this one is incorrect. If you find the answer to the user\'s question, you can respond normally.',
          },
        ],
      });
      screenshot_taken = false;
    } else {
      return ["No Context OR Action Given", page, browser];
    }

    // Process GPT response and handle navigation
    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      max_tokens: 1024,
      messages: messages,
    });

    const message_text = response.choices[0].message.content;
    messages.push({ role: "assistant", content: message_text });

    // Handle navigation based on GPT response
    if (message_text.includes('{"click": "')) {
      await handleLinkNavigation(page, message_text);
    } else if (message_text.includes('{"url": "')) {
    } else {
      return [message_text, page, browser];
    }
  }
  return [openai_final_response, page, browser];
}
