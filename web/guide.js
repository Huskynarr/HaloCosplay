/* Pure helpers for the guide viewer: route validation, link rewriting,
 * heading slugs and the sanitizer policy. No DOM access at load time, so
 * the same file is unit-tested under Node. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.SuitGuide = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  /* A guide path is repo-relative, stays inside the repo and ends in .md.
   * Returns the cleaned path or null. */
  function safeDocPath(raw) {
    if (typeof raw !== 'string' || !raw || raw.length > 300) return null;
    if (/[\u0000-\u001f\u007f\\?#%]/.test(raw)) return null;
    if (raw.charAt(0) === '/' || /^[a-z][a-z0-9+.-]*:/i.test(raw)) return null;
    var parts = raw.split('/');
    for (var i = 0; i < parts.length; i++) {
      if (parts[i] === '' || parts[i] === '.' || parts[i] === '..') return null;
    }
    return /\.md$/i.test(raw) ? raw : null;
  }

  /* "#Dir/File.md#section" -> {file, anchor}. Never throws. */
  function parseRoute(hash) {
    var raw = String(hash || '').replace(/^#/, '');
    if (!raw) return {file: '', anchor: ''};
    var decoded;
    try { decoded = decodeURIComponent(raw); } catch (e) { return {error: 'encoding', raw: raw}; }
    var cut = decoded.indexOf('#');
    var name = cut < 0 ? decoded : decoded.slice(0, cut);
    var anchor = cut < 0 ? '' : decoded.slice(cut + 1);
    if (!/[\/.]/.test(name) && /^[a-z0-9-]+$/.test(name)) return {file: name, anchor: '', sentinel: true};
    var file = safeDocPath(name);
    if (!file) return {error: 'path', raw: decoded};
    return {file: file, anchor: slug(anchor)};
  }

  /* GitHub-style heading slug, ASCII docs only. */
  function slug(text) {
    return String(text || '').trim().toLowerCase()
      .replace(/[^a-z0-9 _-]/g, '').replace(/ /g, '-').slice(0, 120);
  }

  /* Unique ids for a list of heading texts: a, a-1, a-2 ... like GitHub. */
  function headingIds(texts) {
    var seen = {};
    return texts.map(function (text) {
      var base = slug(text), id = base;
      if (Object.prototype.hasOwnProperty.call(seen, base)) { id = base + '-' + seen[base]; seen[base] += 1; }
      else seen[base] = 1;
      return id;
    });
  }

  function dirOf(f) { var i = f.lastIndexOf('/'); return i < 0 ? '' : f.slice(0, i + 1); }
  function normalize(p) {
    var out = [];
    p.split('/').forEach(function (seg) { if (seg === '..') out.pop(); else if (seg !== '.' && seg !== '') out.push(seg); });
    return out.join('/');
  }
  function resolveHref(href, currentFile, topDirs) {
    for (var i = 0; i < topDirs.length; i++) { if (href.indexOf(topDirs[i]) === 0) return normalize(href); }
    return normalize(dirOf(currentFile) + href);
  }

  /* Decide what a link inside a rendered guide becomes.
   * kind: external | anchor | doc | asset | blocked */
  function rewriteLink(href, currentFile, topDirs) {
    href = String(href == null ? '' : href).trim();
    if (/^(https?:|mailto:)/i.test(href)) return {kind: 'external', href: href};
    if (/^[a-z][a-z0-9+.-]*:/i.test(href) || href.indexOf('//') === 0) return {kind: 'blocked'};
    if (href.charAt(0) === '#') return {kind: 'anchor', anchor: slug(decode(href.slice(1))), href: '#' + currentFile + '#' + slug(decode(href.slice(1)))};
    var cut = href.indexOf('#');
    var path = decode(cut < 0 ? href : href.slice(0, cut));
    var anchor = cut < 0 ? '' : slug(decode(href.slice(cut + 1)));
    path = path.split('?')[0];
    if (!path) return {kind: 'blocked'};
    var resolved = resolveHref(path, currentFile, topDirs || []);
    if (!resolved) return {kind: 'blocked'};
    if (/\.md$/i.test(resolved)) {
      if (!safeDocPath(resolved)) return {kind: 'blocked'};
      return {kind: 'doc', file: resolved, anchor: anchor, href: '#' + resolved + (anchor ? '#' + anchor : '')};
    }
    return {kind: 'asset', path: resolved};
  }
  function decode(s) { try { return decodeURIComponent(s); } catch (e) { return s; } }

  /* DOMPurify policy for rendered Markdown: plain content markup only. */
  var purifyConfig = {
    USE_PROFILES: {html: true},
    FORBID_TAGS: ['style', 'form', 'button', 'textarea', 'select', 'option', 'dialog', 'audio', 'video', 'source', 'picture', 'map', 'area', 'nav', 'template'],
    FORBID_ATTR: ['style', 'id', 'name', 'class', 'srcset', 'action', 'formaction', 'autofocus', 'contenteditable', 'tabindex'],
    ALLOW_DATA_ATTR: false,
    ALLOW_ARIA_ATTR: false
  };

  /* Returns sanitized HTML. purify is the DOMPurify instance of the page. */
  function sanitize(purify, html) {
    if (!purify || typeof purify.sanitize !== 'function') throw new Error('sanitizer missing');
    if (!purify.__suitGuideHook) {
      purify.addHook('afterSanitizeAttributes', function (node) {
        // Markdown task lists are the only form control a guide may contain.
        if (node.nodeName === 'INPUT' && String(node.getAttribute('type')).toLowerCase() !== 'checkbox' && node.parentNode) {
          node.parentNode.removeChild(node);
        }
      });
      purify.__suitGuideHook = true;
    }
    return purify.sanitize(String(html), purifyConfig);
  }

  return {safeDocPath: safeDocPath, parseRoute: parseRoute, slug: slug, headingIds: headingIds,
          resolveHref: resolveHref, rewriteLink: rewriteLink, purifyConfig: purifyConfig, sanitize: sanitize};
});
