const { test, expect } = require('@playwright/test');
const { localHtmlUrl, attachRuntimeErrorCollector } = require('./helpers');

test('collection menu opens without JavaScript errors', async ({ page }) => {
  const errors = attachRuntimeErrorCollector(page);
  await page.goto(localHtmlUrl('index.html', 'e2e=1'));
  await expect(page.locator('body')).toBeVisible();
  expect(errors).toEqual([]);
});
