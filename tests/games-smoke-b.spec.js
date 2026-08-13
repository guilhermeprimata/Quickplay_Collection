const { test, expect } = require('@playwright/test');
const { localHtmlUrl, attachRuntimeErrorCollector } = require('./helpers');
async function openClean(page, file) { const errors=attachRuntimeErrorCollector(page); await page.goto(localHtmlUrl(file,'preview=1&e2e=1')); await expect(page.locator('body')).toBeVisible(); await page.waitForTimeout(300); expect(errors).toEqual([]); }
test('Click Speed opens cleanly', async ({ page }) => openClean(page,'click_speed.html'));
test('Corrida de Cavalos opens cleanly', async ({ page }) => openClean(page,'corrida_de_cavalos.html'));
test('Dropworks opens cleanly', async ({ page }) => openClean(page,'dropworks.html'));
