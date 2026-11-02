import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('/opt/node-tools/node_modules/playwright');
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:2});
await p.goto('file://' + process.cwd() + '/poster.html'); await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(300); await p.screenshot({path:'poster-jualan-ebook.png'}); await b.close();
