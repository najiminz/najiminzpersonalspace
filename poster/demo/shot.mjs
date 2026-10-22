import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('/opt/node-tools/node_modules/playwright');
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1240,height:1754}});
for (const n of ['wau-bulan','bas-sekolah']) { await p.goto('file://'+process.cwd()+`/demo/${n}-warna.html`); await p.evaluate(()=>document.fonts.ready); await p.screenshot({path:`demo/${n}-warna.png`}); }
await b.close();
