import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, stat, readdir } from 'node:fs/promises';
import { resolve, join, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('../site/', import.meta.url)));
const mime = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2' };
const server = createServer(async (req, res) => {
  try {
    const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    if (!pathname.startsWith('/review/')) { res.writeHead(404).end(); return; }
    let path = resolve(root, pathname.slice('/review/'.length));
    if (path !== root && !path.startsWith(root + sep)) { res.writeHead(403).end(); return; }
    if ((await stat(path)).isDirectory()) path = join(path, 'index.html');
    res.setHeader('Content-Type', mime[extname(path)] || 'application/octet-stream');
    res.end(await readFile(path));
  } catch { res.writeHead(404).end(); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const origin = `http://127.0.0.1:${server.address().port}`;
let browser;
try {
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const failures = [];
  const external = [];
  page.on('pageerror', error => failures.push(error.message));
  page.on('console', msg => { if (msg.type() === 'error') failures.push(msg.text()); });
  page.on('response', response => { if (response.status() >= 400) failures.push(`${response.status()} ${new URL(response.url()).pathname}`); });
  await page.route('**/*', route => {
    const url = route.request().url();
    if (url.startsWith(origin + '/') || /^(data|blob):/.test(url)) return route.continue();
    external.push(new URL(url).hostname);
    return route.abort();
  });
  const docs = resolve(root, '../docs');
  const mdFiles = [];
  async function walk(dir, prefix = '') {
    for (const entry of await readdir(dir, { withFileTypes: true })) {
      if (entry.isDirectory()) await walk(join(dir, entry.name), prefix + entry.name + '/');
      else if (entry.name.endsWith('.md')) mdFiles.push(prefix + entry.name);
    }
  }
  await walk(docs);
  let diagrams = 0;
  for (const file of mdFiles) {
    const md = await readFile(join(docs, file), 'utf8');
    const count = (md.match(/^```mermaid\s*$/gm) || []).length;
    const route = file.endsWith('index.md') ? file.slice(0, -'index.md'.length) : file.replace(/\.md$/, '/');
    await page.goto(`${origin}/review/${route}`, { waitUntil: 'networkidle' });
    if (count) {
      await page.waitForFunction(n => document.querySelectorAll('.review-diagram svg').length === n, count, { timeout: 30000 });
      diagrams += count;
    }
    if (await page.locator('[data-diagram-error]').count()) failures.push(`Mermaid: ${file}`);
    if (!(await page.locator('h1').count())) failures.push(`Titolo assente: ${file}`);
  }
  await page.goto(origin + '/review/', { waitUntil: 'networkidle' });
  await page.locator('input.md-search__input').click();
  await page.locator('input.md-search__input').pressSequentially('revoca', { delay: 100 });
  await page.waitForFunction(() => document.querySelectorAll('.md-search-result__link').length > 0).catch(async error => {
    console.error(JSON.stringify({ failures, external, search: await page.locator('.md-search-result').innerText() }));
    throw error;
  });
  const searchResults = await page.locator('.md-search-result__link').count();
  await page.keyboard.press('Escape');
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(origin + '/review/en/06-dpp-analysis/', { waitUntil: 'networkidle' });
  await page.waitForSelector('.review-diagram svg');
  const mobile = await page.evaluate(() => ({ width: window.innerWidth, content: document.documentElement.scrollWidth }));
  if (mobile.content > mobile.width + 2) failures.push('Overflow orizzontale viewport mobile');
  const menu = page.locator('.md-header__button[for="__drawer"]');
  await menu.click();
  const drawerOpen = await page.locator('#__drawer').isChecked();
  if (!drawerOpen) failures.push('Menu mobile non aperto');
  if (external.length) failures.push('Dipendenze di rete esterne: ' + [...new Set(external)].join(', '));
  const report = { pages: mdFiles.length, mermaid_rendered: diagrams, search_results: searchResults,
    repository_subpath: '/review/', mobile, mobile_menu: drawerOpen, external_requests: external.length, errors: failures };
  console.log(JSON.stringify(report, null, 2));
  if (failures.length) process.exitCode = 1;
} finally {
  if (browser) await browser.close();
  await new Promise(resolve => server.close(resolve));
}
