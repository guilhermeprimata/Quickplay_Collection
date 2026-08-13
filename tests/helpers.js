const { expect } = require('@playwright/test');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const START_SELECTORS = ['#play','#start','#startBtn','#startGame','#newGame','#new-game','#btnStart','[data-action="start"]'];
const START_TEXT = /^(novo jogo|nova partida|jogar|jogue|começar|iniciar|play|start|new game|new run|survival|arcade|classic|clássico)/i;

function localHtmlUrl(file, query = '') {
  const url = pathToFileURL(path.join(process.cwd(), file));
  if (query) url.search = query;
  return url.href;
}

function attachRuntimeErrorCollector(page) {
  const errors = [];
  page.on('pageerror', error => errors.push(`pageerror: ${error.message}`));
  page.on('console', message => {
    if (message.type() === 'error') errors.push(`console: ${message.text()}`);
  });
  return errors;
}

async function clickStartIfPresent(page) {
  for (const selector of START_SELECTORS) {
    const locator = page.locator(selector).first();
    if (await locator.count() && await locator.isVisible().catch(() => false)) {
      await locator.click({ timeout: 3000 });
      return selector;
    }
  }
  const byText = page.getByRole('button', { name: START_TEXT }).first();
  if (await byText.count() && await byText.isVisible().catch(() => false)) {
    await byText.click({ timeout: 3000 });
    return 'button-text';
  }
  return null;
}

async function expectHealthyDocument(page) {
  await expect(page.locator('body')).toBeVisible();
  const dimensions = await page.evaluate(() => ({
    width: document.documentElement.scrollWidth,
    height: document.documentElement.scrollHeight,
    textLength: (document.body?.innerText || '').trim().length,
    surfaces: document.querySelectorAll('canvas,svg,main,button,input,select').length
  }));
  expect(dimensions.width).toBeGreaterThan(0);
  expect(dimensions.height).toBeGreaterThan(0);
  expect(dimensions.textLength + dimensions.surfaces).toBeGreaterThan(0);
}

async function exerciseBasicControls(page) {
  for (const key of ['ArrowRight','ArrowUp','ArrowLeft']) {
    await page.keyboard.down(key);
    await page.waitForTimeout(120);
    await page.keyboard.up(key);
  }
}

module.exports = { localHtmlUrl, attachRuntimeErrorCollector, clickStartIfPresent, expectHealthyDocument, exerciseBasicControls };
