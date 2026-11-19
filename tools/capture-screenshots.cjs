/* Capture actual prototype UI with disposable synthetic state; no live Retell calls. */
const { spawn } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const net = require("node:net");
const { setTimeout: delay } = require("node:timers/promises");
const root = path.resolve(__dirname, "..");
const { chromium } = require(require.resolve("playwright", { paths: [path.join(root, "frontend")] }));
const output = path.join(root, "assets/screenshots");
const temp = fs.mkdtempSync(path.join(os.tmpdir(), "speedq-portfolio-"));
const python = process.env.BEACON_PYTHON || path.join(root, "backend/.venv", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
let server, browser, logs = "";

async function freePort() {
  const listener = net.createServer();
  await new Promise((resolve, reject) => {
    listener.once("error", reject);
    listener.listen(0, "127.0.0.1", resolve);
  });
  const port = listener.address().port;
  await new Promise(resolve => listener.close(resolve));
  return port;
}

(async () => {
  const base = `http://127.0.0.1:${await freePort()}`;
  server = spawn(python, ["-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", new URL(base).port, "--no-access-log"], {
    cwd: path.join(root, "backend"),
    env: { ...process.env, NRY_DB: path.join(temp, "capture.db"), NRY_NOW: "2026-11-15T12:00:00Z", NRY_STAFF_PASSWORD: "", NRY_STAFF_ACCOUNTS: "", NRY_WEBHOOK_SECRET: "", RETELL_API_KEY: "" },
    stdio: ["ignore", "pipe", "pipe"],
  });
  server.on("error", e => { logs += e.message; });
  server.stdout.on("data", b => { logs += b; });
  server.stderr.on("data", b => { logs += b; });
  let ready = false;
  for (let i = 0; i < 100; i++) {
    try { ready = (await fetch(base + "/workspace/session")).ok; } catch {}
    if (ready) break;
    if (server.exitCode !== null) break;
    await delay(100);
  }
  if (!ready) throw new Error("Capture server unavailable: " + logs);
  browser = await chromium.launch({
    ...(process.env.BEACON_CHROMIUM ? { executablePath: process.env.BEACON_CHROMIUM } : fs.existsSync("/usr/bin/chromium") ? { executablePath: "/usr/bin/chromium" } : {}),
    headless: true,
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 }, reducedMotion: "reduce" });
  const errors = [];
  page.on("pageerror", e => errors.push(e.message));
  await page.goto(base);
  await page.waitForFunction(() => document.getElementById("sync-label").textContent.startsWith("Live"));
  await page.getByRole("button", { name: "Load sample cases", exact: true }).click();
  await page.getByRole("button", { name: "Add sample cases", exact: true }).click();
  await page.locator(".case-row").nth(4).waitFor();
  await page.getByRole("button", { name: /^Preview Maria/ }).click();
  await page.locator("#overview h2").filter({ hasText: "Maria" }).waitFor();
  fs.mkdirSync(output, { recursive: true });
  async function capture(name, fullPage = false) {
    await page.locator("#toast").waitFor({ state: "hidden" });
    await page.evaluate(() => document.activeElement.blur());
    await page.screenshot({ path: path.join(output, name), fullPage, animations: "disabled" });
  }
  await capture("dashboard-desktop.png");
  await page.getByRole("button", { name: "Care insights", exact: true }).click();
  await page.waitForFunction(() => document.getElementById("insights-content").innerText.includes("$5,539.00"));
  await capture("care-insights.png", true);
  await page.getByRole("button", { name: /^Priority queue/ }).first().click();
  await page.getByRole("button", { name: /^Preview Maria/ }).click();
  await page.getByRole("button", { name: "Review case", exact: true }).click();
  await page.locator("#detail-view h1").filter({ hasText: "Maria" }).waitFor();
  await capture("case-review.png");
  if (errors.length) throw new Error(errors.join("; "));
  fs.writeFileSync(path.join(output, "README.md"), `# Prototype screenshots\n\nCaptured ${new Date().toISOString().slice(0, 10)} with [tools/capture-screenshots.cjs](../../tools/capture-screenshots.cjs). Actual running UI, 1600px viewport, isolated synthetic database, no live service.\n\n- [Priority queue](dashboard-desktop.png)\n- [Care insights](care-insights.png)\n- [Case review](case-review.png)\n\nCase counts, dates and waiting times are illustrative, not production measurements. The headset is original project artwork.\n`);
  console.log("Captured three current UI screenshots; no browser JavaScript errors.");
})().catch(e => { console.error(e); process.exitCode = 1; }).finally(async () => {
  if (browser) await browser.close();
  if (server && server.exitCode === null) {
    server.kill("SIGTERM");
    await Promise.race([new Promise(resolve => server.once("exit", resolve)), delay(3000)]);
    if (server.exitCode === null) {
      server.kill("SIGKILL");
      await new Promise(resolve => server.once("exit", resolve));
    }
  }
  fs.rmSync(temp, { recursive: true, force: true });
});
