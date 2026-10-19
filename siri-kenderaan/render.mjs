// Screenshots build/*.html to build/*.png at A4 @ 300 DPI (2480 x 3508 px).
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || 'playwright');
import { readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const build = process.env.BUILD_DIR || join(dirname(fileURLToPath(import.meta.url)), 'build');
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 2480, height: 3508 }, deviceScaleFactor: 1 });
for (const f of readdirSync(build).filter((f) => f.endsWith('.html')).sort()) {
  await page.goto('file://' + join(build, f));
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: join(build, f.replace('.html', '.png')), fullPage: false });
  console.log('rendered', f);
}
await browser.close();
