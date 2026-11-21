const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const canonical = JSON.parse(fs.readFileSync(path.join(root, 'courses.json'), 'utf8'));
const generated = fs.readFileSync(path.join(root, 'courses-data.js'), 'utf8');

test('offline projection mirrors canonical catalog', () => {
  const window = {};
  vm.runInNewContext(generated, {window});
  assert.deepEqual(JSON.parse(JSON.stringify(window.COURSE_CATALOG)), canonical);
});

test('all 28 chapter paths exist and are sequential', () => {
  assert.equal(canonical.chapters.length, 28);
  canonical.chapters.forEach((chapter, index) => {
    const number = String(index + 1).padStart(2, '0');
    assert.equal(chapter.num, number);
    assert.equal(chapter.file, number + '.html');
    assert.ok(fs.existsSync(path.join(root, chapter.file)));
    assert.ok(chapter.category);
    assert.ok(chapter.tags.length > 0);
  });
});

test('homepage loads a local catalog and exposes search/category/tag filters', () => {
  assert.match(html, /<script src="courses-data\.js"><\/script>/);
  assert.match(html, /id="course-search"/);
  assert.match(html, /id="category-select"/);
  assert.match(html, /id="category-filters"/);
  assert.match(html, /id="tag-filters"/);
  assert.doesNotMatch(html, /fetch\s*\(/);
  assert.doesNotMatch(html, /XMLHttpRequest/);
});

test('homepage renders chapter metadata with textContent rather than innerHTML', () => {
  assert.match(html, /title\.textContent\s*=\s*chapter\.title/);
  assert.match(html, /summary\.textContent\s*=\s*chapter\.summary/);
  assert.match(html, /link\.href\s*=\s*chapter\.file/);
  assert.doesNotMatch(html, /\.innerHTML\s*=/);
});

test('first five chapters are deeply revised and have evidence ledgers', () => {
  for (let index = 1; index <= 5; index++) {
    const number = String(index).padStart(2, '0');
    const article = fs.readFileSync(path.join(root, number + '.html'), 'utf8');
    const evidence = JSON.parse(fs.readFileSync(path.join(root, 'evidence', number + '.json'), 'utf8'));
    assert.match(article, /<h1>/);
    assert.match(article, /<main/);
    assert.match(article, /<figure/);
    assert.ok(evidence.claims.length >= 3);
  }
});

test('second batch chapters expose accessible interactive exercises and verified evidence', () => {
  for (let index = 6; index <= 10; index++) {
    const number = String(index).padStart(2, '0');
    const article = fs.readFileSync(path.join(root, number + '.html'), 'utf8');
    const evidence = JSON.parse(fs.readFileSync(path.join(root, 'evidence', number + '.json'), 'utf8'));
    assert.match(article, /aria-live="polite"/);
    assert.match(article, /<figure class="diagram">/);
    assert.match(article, /<footer class="article-footer">/);
    assert.ok(evidence.claims.length >= 5);
    for (const claim of evidence.claims) {
      assert.ok(claim.source_url, number + ': ' + claim.id + ' missing source_url');
      assert.ok(claim.locator, number + ': ' + claim.id + ' missing locator');
    }
  }
});
