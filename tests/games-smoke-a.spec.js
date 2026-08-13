const { test, expect } = require('@playwright/test');
const { localHtmlUrl, attachRuntimeErrorCollector } = require('./helpers');

async function openClean(page, file) {
  const errors = attachRuntimeErrorCollector(page);
  await page.goto(localHtmlUrl(file, 'preview=1&e2e=1'));
  await expect(page.locator('body')).toBeVisible();
  await page.waitForTimeout(300);
  expect(errors).toEqual([]);
}

test('Adivinhe o Número opens cleanly', async ({ page }) => openClean(page, 'advinhe_o_numero.html'));
test('Bow and Arrow opens cleanly', async ({ page }) => openClean(page, 'bow_and_arrow.html'));
test('Toxic Stench opens cleanly', async ({ page }) => openClean(page, 'campo_minado.html'));
