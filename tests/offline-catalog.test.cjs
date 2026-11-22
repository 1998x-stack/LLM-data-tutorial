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

test('third batch chapters 11-15 expose interactive exercises and evidence ledgers', () => {
  for (let index = 11; index <= 15; index++) {
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

test('batch 03 mathematical expressions use semantic MathML, not unrendered TeX', () => {
  for (let index = 11; index <= 14; index++) {
    const number = String(index).padStart(2, '0');
    const article = fs.readFileSync(path.join(root, number + '.html'), 'utf8');
    assert.match(article, /<math/);
    assert.equal(article.includes(String.fromCharCode(92) + '('), false);
  }
});

test('fourth batch chapters 16-20 expose interactive exercises and evidence ledgers', () => {
  const controls = {
    16: ['raw-size', 'compression-ratio', 'file-target'],
    17: ['run-source', 'run-code', 'run-config', 'run-tokenizer'],
    18: ['margin-error'],
    19: ['merge-count'],
    20: ['vocab-size', 'hidden-size', 'weight-bytes', 'tied-weights'],
  };
  for (let index = 16; index <= 20; index++) {
    const number = String(index).padStart(2, '0');
    const article = fs.readFileSync(path.join(root, number + '.html'), 'utf8');
    const evidence = JSON.parse(fs.readFileSync(path.join(root, 'evidence', number + '.json'), 'utf8'));
    assert.match(article, /<h1>/);
    assert.match(article, /<main/);
    assert.match(article, /<figure class="diagram">/);
    assert.match(article, /<footer class="article-footer">/);
    assert.match(article, /aria-live="polite"/);
    assert.equal(article.includes(String.fromCharCode(92) + '('), false);
    for (const id of controls[index]) assert.ok(article.includes('id="' + id + '"'), number + ': missing control ' + id);
    assert.ok(evidence.claims.length >= 7);
    for (const claim of evidence.claims) {
      assert.ok(claim.source_url, number + ': ' + claim.id + ' missing source_url');
      assert.ok(claim.locator, number + ': ' + claim.id + ' missing locator');
    }
  }
});

test('chapters 18-20 render substantive equations as MathML', () => {
  for (let index = 18; index <= 20; index++) {
    const number = String(index).padStart(2, '0');
    const article = fs.readFileSync(path.join(root, number + '.html'), 'utf8');
    assert.match(article, /<math/);
    assert.match(article, /aria-label=/);
  }
});

test('fifth batch chapters 21-25 expose accessible exercises and evidence ledgers', () => {
  const controls = {
    21: ['syn-count', 'syn-schema', 'syn-verify', 'syn-unique', 'syn-safe'],
    22: ['domain-total', 'domain-share'],
    23: ['dt-files', 'dt-tasks', 'dt-workers'],
    24: ['bloom-n', 'bloom-p'],
    25: ['clean-tp', 'clean-fp', 'clean-fn'],
  };
  for (let index = 21; index <= 25; index++) {
    const number = String(index).padStart(2, '0');
    const article = fs.readFileSync(path.join(root, number + '.html'), 'utf8');
    const evidence = JSON.parse(fs.readFileSync(path.join(root, 'evidence', number + '.json'), 'utf8'));
    assert.match(article, /<h1>/);
    assert.match(article, /<main/);
    assert.match(article, /<figure class="diagram">/);
    assert.match(article, /<footer class="article-footer">/);
    assert.match(article, /aria-live="polite"/);
    assert.equal(article.includes(String.fromCharCode(92) + '('), false);
    for (const id of controls[index]) assert.ok(article.includes('id="' + id + '"'), number + ': missing control ' + id);
    assert.ok(evidence.claims.length >= 5, number + ": expected five or more independently sourced claims");
    for (const claim of evidence.claims) {
      assert.ok(claim.source_url, number + ': ' + claim.id + ' missing source_url');
      assert.ok(claim.locator, number + ': ' + claim.id + ' missing locator');
    }
  }
});

test('fifth batch equations use semantic MathML', () => {
  for (let index = 21; index <= 25; index++) {
    const number = String(index).padStart(2, '0');
    const article = fs.readFileSync(path.join(root, number + '.html'), 'utf8');
    assert.match(article, /<math/);
    assert.match(article, /aria-label=/);
  }
});


test('sixth batch 26–28: semantic structure, math, diagrams, evidence and controls', () => {
  const controls = {
    26: ['gate-kept', 'gate-audited', 'gate-hard', 'gate-result'],
    27: ['mix-web', 'mix-code', 'mix-math', 'mix-temp', 'mix-explore', 'mix-output'],
    28: ['cap-min-accepted', 'cap-max-reject', 'cap-output'],
  };
  for (let index = 26; index <= 28; index++) {
    const number = String(index).padStart(2, '0');
    const article = fs.readFileSync(path.join(root, number + '.html'), 'utf8');
    const evidence = JSON.parse(fs.readFileSync(path.join(root, 'evidence', number + '.json'), 'utf8'));
    assert.match(article, /<h1>/);
    assert.match(article, /<main/);
    assert.match(article, /<nav/);
    assert.match(article, /<article/);
    assert.match(article, /<math/);
    assert.match(article, /<figure class="diagram">/);
    assert.match(article, /<footer class="article-footer">/);
    assert.match(article, /aria-live="polite"/);
    assert.equal(article.includes(String.fromCharCode(92) + '('), false);
    assert.ok(evidence.claims.length >= 8);
    for (const id of controls[index]) assert.ok(article.includes('id="' + id + '"'), number + ': missing ' + id);
    for (const claim of evidence.claims) {
      for (const key of ['id', 'claim', 'kind', 'status', 'source_url', 'locator', 'notes']) {
        assert.ok(String(claim[key] || '').trim(), number + ': missing claim field ' + key);
      }
    }
    const scripts = Array.from(article.matchAll(/<script>([\s\S]*?)<\/script>/g), m => m[1]);
    assert.equal(scripts.length, 1, number + ': expected one local interaction script');
    assert.doesNotThrow(() => new vm.Script(scripts[0]), number + ': invalid JavaScript syntax');
  }
});

test('all 28 chapters have refined metadata and valid prior prerequisites', () => {
  assert.match(html, /<strong>01–28<\/strong><span>深度重构章节<\/span>/);
  for (const chapter of canonical.chapters) {
    assert.equal(chapter.status, 'refined', chapter.num);
    for (const prereq of chapter.prerequisites || []) {
      assert.ok(Number(prereq) < Number(chapter.num), chapter.num + ': invalid prerequisite ' + prereq);
    }
  }
});
