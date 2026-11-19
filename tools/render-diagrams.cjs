/* Export the editable workflow SVG to PNG without altering the source artwork. */
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "..");
const { chromium } = require(require.resolve("playwright", { paths: [path.join(root, "frontend")] }));
(async () => {
  const browser = await chromium.launch({
    ...(process.env.BEACON_CHROMIUM ? { executablePath: process.env.BEACON_CHROMIUM } : fs.existsSync("/usr/bin/chromium") ? { executablePath: "/usr/bin/chromium" } : {}),
    headless: true,
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1600, height: 1140 }, deviceScaleFactor: 1 });
    await page.setContent("<!doctype html><style>html,body{margin:0}</style>" + fs.readFileSync(path.join(root, "assets/diagrams/pipeline.svg"), "utf8"));
    await page.evaluate(() => document.fonts.ready);
    await page.locator("svg").screenshot({ path: path.join(root, "assets/diagrams/pipeline.png") });
    console.log("Rendered assets/diagrams/pipeline.png from the editable SVG.");
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
