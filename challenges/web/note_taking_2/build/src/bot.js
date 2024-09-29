const puppeteer = require("puppeteer");
const fs = require("fs");

async function visit(flag_id, id, title) {
  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--headless"],
    executablePath: "/usr/bin/chromium",
  });

  try {
    let page = await browser.newPage();

    await page.setCookie({
      name: "uid",
      value: flag_id,
      domain: "localhost",
      httpOnly: true,
    });

    page = await browser.newPage();

    await page.goto(`http://localhost:3000/`, { timeout: 5000 });

    console.log("Step 1 done!");

    await new Promise((resolve) => setTimeout(resolve, 5000));

    await page.goto(`http://localhost:3000/?id=${id}&title=${title}`, {
      timeout: 5000,
    });

    console.log("Step 2 done!");

    await new Promise((resolve) => setTimeout(resolve, 5000));

    await page.close();
    await browser.close();
  } catch (e) {
    console.log(e);
    await browser.close();
  }
}

module.exports = { visit };

