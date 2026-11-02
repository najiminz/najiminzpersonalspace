// Records video.html frame by frame (exact timing) and writes the PNG frames for ffmpeg.
import { createRequire } from 'module';
import { mkdirSync } from 'fs';
const { chromium } = createRequire(import.meta.url)('/opt/node-tools/node_modules/playwright');
const [, , mode = 'full', fps = '30', secs = '26'] = process.argv;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file://' + process.cwd() + '/' + (process.env.PAGE || 'video.html')); await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(500);
if (mode === 'check') {
  for (const t of (process.env.TIMES || '3.5,6,12.5,17.5,23').split(',').map(Number)) { await p.evaluate(t => seek(t), t); await p.screenshot({ path: `check-${t}.png` }); }
} else {
  mkdirSync('frames', { recursive: true });
  const n = Math.round(+secs * +fps);
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => seek(t), i / +fps);
    await p.screenshot({ path: `frames/f${String(i).padStart(4, '0')}.png` });
  }
}
await b.close();
