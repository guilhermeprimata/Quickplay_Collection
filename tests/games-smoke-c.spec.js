const { test, expect } = require('@playwright/test');
const { localHtmlUrl, attachRuntimeErrorCollector } = require('./helpers');
async function openClean(page, file) { const errors=attachRuntimeErrorCollector(page); await page.goto(localHtmlUrl(file,'preview=1&e2e=1')); await expect(page.locator('body')).toBeVisible(); await page.waitForTimeout(300); expect(errors).toEqual([]); }
test('Foguetinho opens cleanly', async ({ page }) => openClean(page,'foguetinho.html'));
test('Idle Trader opens cleanly', async ({ page }) => openClean(page,'idle_trader.html'));
test('Jogo da Forca opens cleanly', async ({ page }) => openClean(page,'jogo_da_forca.html'));
