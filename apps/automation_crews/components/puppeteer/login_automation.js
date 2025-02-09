import StealthPlugin from "puppeteer-extra-plugin-stealth";
import puppeteer from "puppeteer-extra";
import readline from "readline";
import dotenv from "dotenv";
dotenv.config();
import { readPromptFromFile, askQuestion } from "./helper.js";
import { fetchEmailsAndAttachments } from "./components/puppeteer/automation_response.js";
const stealth = StealthPlugin();
stealth.enabledEvasions.delete("iframe.contentWindow");
stealth.enabledEvasions.delete("media.codecs");
puppeteer.use(stealth);

export async function loginGoogle_navigateToGmail(userInput) {
  const browser = await puppeteer.launch({
    headless: "new",
  });
  const page = await browser.newPage();
  await page.setViewport({
    width: 1200,
    height: 1200,
    deviceScaleFactor: 1.75,
  });

  // Read GPT main prompt from text file
  const main_prompt = await readPromptFromFile(
    "./src/components/puppeteer/prompts/openai_prompt.txt"
  );
  const messages = [
    {
      role: "system",
      content: main_prompt,
    },
  ];
  const prompt = userInput;
  console.log(prompt);
  messages.push({ role: "user", content: prompt });

  // Initialize variables
  let url = process.env.LOGIN_URL;
  let action_exists = false;
  let email = process.env.EMAIL;
  let phone = process.env.PHONE;
  let password = process.env.PASSWORD;
  let login_status = false;
  let action = "";

  // Get action from User input
  if (prompt.toLowerCase()) {
    const actionMatch = prompt.match(/Action:(\S+)/);
    if (actionMatch) {
      action = actionMatch[1];
      action_exists = true;
    }
  }

  // Navigate to requested URL
  while (true) {
    if (url) {
      await page.goto(url, {
        waitUntil: "domcontentloaded",
      });
      if (email && password) {
        try {
          // Wait for the email input and fill it
          await page.waitForSelector('input[type="email"]', { timeout: 60000 });
          await page.type('input[type="email"]', email);

          // Click the next button after entering the email
          const emailNextButtonSelector = "#identifierNext";
          await page.waitForSelector(emailNextButtonSelector, {
            timeout: 60000,
          });
          await page.click(emailNextButtonSelector);

          // Wait for navigation to the password page
          await page.waitForNavigation({ waitUntil: "networkidle0" });

          // Wait for the password input to appear
          await page.waitForSelector('input[type="password"]', {
            timeout: 60000,
          });
          await page.type('input[type="password"]', password);

          // Click the next button after entering the password
          const passwordNextButtonSelector = "#passwordNext";
          await page.waitForSelector(passwordNextButtonSelector, {
            timeout: 60000,
          });

          // Ensure the button is visible and enabled
          const passwordNextButton = await page.$(passwordNextButtonSelector);
          await page.evaluate(
            (button) => button.scrollIntoView(),
            passwordNextButton
          );
          await page.waitForFunction(
            (button) => button && !button.disabled,
            {},
            passwordNextButton
          );

          console.log("Clicking the password next button...");
          await passwordNextButton.click();

          // Wait for the navigation to complete after logging in
          await page.waitForNavigation({ waitUntil: "networkidle0" });

          // Wait for the 2FA to appear and ensure it's visible
          const phoneNumberInput = await page.waitForSelector(
            'input[type="tel"]',
            { timeout: 60000, visible: true }
          );
          await phoneNumberInput.type(phone);

          // Wait for the "Send" button to appear and ensure it's clickable
          const sendButtonSelector = 'button[type="button"] span.VfPpkd-vQzf8d';
          await page.waitForSelector(sendButtonSelector, { visible: true });

          // Scroll the "Send" button into view
          await page.evaluate((selector) => {
            document.querySelector(selector).scrollIntoView();
          }, sendButtonSelector);

          // Wait for a short moment to ensure the button is clickable
          await new Promise((r) => setTimeout(r, 500));

          // Click the "Send" button
          await page.click(sendButtonSelector);
          await page.waitForNavigation({ waitUntil: "networkidle0" });

          // Prompt the user to enter the verification code
          const verificationCode = await askQuestion(
            "Please enter your Verification Code: "
          );

          // Wait for the 2FA to appear and ensure it's visible
          const verificationNumberInput = await page.waitForSelector(
            'input[type="tel"]',
            { timeout: 60000, visible: true }
          );
          await verificationNumberInput.type(verificationCode);

          try {
            // Click the login button
            await page.click(
              ".VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.BqKGqe.Jskylb.TrZEUc.lw1w4b"
            );
            // Wait for navigation
            await page.waitForNavigation();
            login_status = true;

            const [result, updatedPage, updatedBrowser] =
              await fetchEmailsAndAttachments(userInput, page, browser);

            // Return response data
            return [result, updatedPage, login_status, updatedBrowser];
          } catch (error) {
            console.log("Login failed or navigation error:", error);
          }
        } catch (error) {
          console.log("Error during login process:", error);
        }
      }
    }
  }
}
