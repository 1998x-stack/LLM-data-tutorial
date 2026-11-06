const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const canonical = JSON.parse(fs.readFileSync(path.join(root, 'courses.json'), 'utf8'));
const generated = fs.readFileSync(path.join(root, 'courses-data.js'), 'utf8');
const script = html.match(/<script>\s*([\s\S]*?)<\/script>/)?.[1];
class Element {
  constructor() { this.children = []; this.className = ''; this.href = ''; this._text = ''; }
  set textContent(value) { this._text = String(value); this.children = []; }
  get textContent() { return this._text + this.children.map(x => x.textContent).join(''); }
  appendChild(x) { this.children.push(x); return x; }
  replaceChildren(...nodes) { this._text = ''; this.children = nodes; }
}
function render(manifest) {
  const elements = new Map();
  const container = new Element();
  const document = {
    title: '',
    getElementById: id => id === 'cardContainer' ? container : null,
    querySelector: key => { if (!elements.has(key)) elements.set(key, new Element()); return elements.get(key); },
    createElement: () => new Element(),
  };
  vm.runInNewContext(script, {window: {COURSE_CATALOG: manifest}, document, fetch: () => {throw Error('fetch forbidden');}});
  return {container, document};
}
test('offline data mirrors canonical JSON', () => {
  const window = {};
  vm.runInNewContext(generated, {window});
  assert.deepEqual(JSON.parse(JSON.stringify(window.COURSE_CATALOG)), canonical);
});
test('renders 28 local chapter links without fetch', () => {
  assert.ok(script);
  assert.ok(html.includes('<script src="courses-data.js"></script>'));
  const {container} = render(canonical);
  assert.equal(container.children.length, 28);
  for (let i = 0; i < 28; i++) {
    const link = container.children[i].children.at(-1).children[0];
    assert.equal(link.href, String(i + 1).padStart(2, '0') + '.html');
    assert.ok(fs.existsSync(path.join(root, link.href)));
  }
});
test('missing data shows a visible error', () => {
  assert.equal(render(undefined).container.children[0].className, 'state-msg error');
});
test('invalid chapter URL is rejected', () => {
  const bad = {...canonical, chapters: [{num:'01', title:'bad', topics:[], file:'javascript:alert(1)'}]};
  assert.equal(render(bad).container.children[0].className, 'state-msg error');
});
test('untrusted chapter title stays plain text', () => {
  const title = '<img src=x onerror=alert(1)>';
  const {container} = render({...canonical, chapters: [{num:'01',title,topics:[],file:'01.html'}]});
  assert.equal(container.children[0].children[0].children[1].textContent, title);
});
