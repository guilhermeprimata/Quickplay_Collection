const { test, expect } = require('@playwright/test');
const { localHtmlUrl, attachRuntimeErrorCollector } = require('./helpers');

test('Snowball Avalanche starts and advances', async ({ page }) => {
  const errors = attachRuntimeErrorCollector(page);
  await page.goto(localHtmlUrl('snowball_avalanche.html', 'e2e=1'));
  await expect(page.locator('#play')).toBeVisible();
  await page.locator('#play').click();
  await expect(page.locator('#hud')).toBeVisible();
  const before = await page.locator('#hudDistance').textContent();
  await page.waitForTimeout(1500);
  const after = await page.locator('#hudDistance').textContent();
  expect(after).not.toBe(before);
  expect(errors).toEqual([]);
});
