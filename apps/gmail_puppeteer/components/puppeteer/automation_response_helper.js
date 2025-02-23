import fs from "fs";
import path from "path";
import pdf from "pdf-parse";
import {
  downloadEmailAttachement,
  imageToBase64,
  highlightLinks,
} from "./helper.js";
export async function processAllFiles(folderPath) {
  const files = await fs.promises.readdir(folderPath);
  let allText = "";

  for (const file of files) {
    if (path.extname(file).toLowerCase() === ".pdf") {
      const dataBuffer = await fs.promises.readFile(
        path.join(folderPath, file)
      );
      const data = await pdf(dataBuffer);
      allText += data.text + "\n";
    }
  }

  return allText;
}

export async function handleEmailNavigation(page) {
  try {
    await page.waitForSelector("tr.zA.zE", { visible: true });
    const firstUnreadEmail = await page.$("tr.zA.zE");

    if (firstUnreadEmail) {
      await firstUnreadEmail.click({ delay: 100 });
      return [true, false, ""];
    }

    return [false, false, "No Unread email found"];
  } catch (error) {
    console.error("Error navigating email:", error);
    return [false, false, "No Unread email found"];
  }
}

export async function handleAttachmentDownload(page) {
  try {
    await page.waitForSelector("a.aQy.aZr.e");
    const attachmentUrl = await page.evaluate(() => {
      const anchor = document.querySelector("a.aQy.aZr.e");
      if (anchor) {
        let url = anchor.href;
        return url.replace("disp=inline", "disp=safe");
      }
      return null;
    });

    return await downloadEmailAttachement(page, attachmentUrl);
  } catch (error) {
    console.error("Error handling attachment:", error);
    return false;
  }
}

export async function processGPTResponse(
  messages,
  openai,
  hasAttachment,
  folderPath
) {
  // Process email screenshot
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
        text: "Here's the screenshot of the email just Give me the Summary of Email in bullet points.",
      },
    ],
  });

  const emailResponse = await openai.chat.completions.create({
    model: "gpt-4o",
    max_tokens: 1024,
    messages: messages,
  });

  const emailSummary = emailResponse.choices[0].message.content;
  messages.push({ role: "assistant", content: emailSummary });

  // Process attachment if present
  let attachmentSummary = "";
  if (hasAttachment) {
    const extractedText = await processAllFiles(folderPath);

    messages.push({
      role: "user",
      content: [
        {
          type: "text",
          text: `As an helpful assistant read the below context carefully and provide the Account summary from given bank statement in bullet points Only. Remember that do not include any information which is not relevant to context. If context not given then say Email has no attachment.\nCONTEXT: ${extractedText}.\nExample Response:`,
        },
      ],
    });

    const attachmentResponse = await openai.chat.completions.create({
      model: "gpt-4o",
      max_tokens: 1024,
      messages: messages,
    });

    attachmentSummary = attachmentResponse.choices[0].message.content;
  }

  return `
    **# Email Summary #** \n
    ${emailSummary}
    
    **# Email Attachment Summary #** \n
    ${attachmentSummary || "No attachment found"}`;
}

export async function handleLinkNavigation(page, message_text) {
  try {
    const linkText = message_text
      .split('{"click": "')[1]
      .split('"}')[0]
      .replace(/[^a-zA-Z0-9 ]/g, "")
      .toLowerCase();

    if (linkText !== "compose") {
      const navigationUrl = `https://mail.google.com/mail/u/0/#${linkText}`;
      await page.goto(navigationUrl);
      await page.waitForNavigation({ waitUntil: "networkidle2" });

      await highlightLinks(page);
      await page.screenshot({ path: "screenshot.jpg", quality: 100 });

      return true;
    } else {
      return true;
    }
  } catch (error) {
    return false;
  }
}
