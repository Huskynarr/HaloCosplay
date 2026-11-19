(function () {
  'use strict';

  if (window.HaloMonitoring) return;

  // Public client DSN only. The administration token never belongs in this file.
  const DSN = 'https://0d3226ac2cb6712901dd6bc0942f4b69@logging.gardenpiratez.de/57';
  const SDK_URL = 'https://browser.sentry-cdn.com/11.14.0/bundle.min.js';
  const SDK_INTEGRITY = 'sha384-jCAqT6eX+TSYGAhAPoGRdVSau37cLPr0E7njTbruV95FY3W1LVq5TAi+/QIwOIy5';
  const options = window.HaloMonitoringOptions || {};
  const local = location.protocol !== 'https:' ||
    /^(localhost|.*\.localhost|127(?:\.\d+){3}|\[::1\])$/.test(location.hostname);
  const enabled = options.enabled === true || (options.enabled !== false && !local);
  const pending = [];
  let sdk = null;
  let stopped = !enabled;

  function captureException(error, operation, mechanism) {
    if (stopped) return;
    const hint = {captureContext: {tags: {operation: operation || 'unhandled'}}};
    if (mechanism) hint.mechanism = mechanism;
    if (sdk) return sdk.captureException(error, hint);
    if (pending.length < 20) pending.push({error, operation, mechanism});
  }

  window.HaloMonitoring = Object.freeze({captureException});
  if (!enabled) return;

  function earlyError(event) {
    // Resource failures have no ErrorEvent.message and are not JS exceptions.
    if (event.message) captureException(event.error || new Error(event.message),
      'unhandled', {handled: false, type: 'onerror'});
  }

  function earlyRejection(event) {
    captureException(event.reason, 'unhandled', {handled: false, type: 'onunhandledrejection'});
  }

  function stopBuffering() {
    window.removeEventListener('error', earlyError);
    window.removeEventListener('unhandledrejection', earlyRejection);
  }

  function fail() {
    stopped = true;
    pending.length = 0;
    stopBuffering();
  }

  function cleanUrl(value) {
    if (!value) return value;
    try {
      const url = new URL(value, location.href);
      return /^https?:$/.test(url.protocol) ? url.origin + url.pathname : '[non-http URL]';
    } catch (_) { return '[invalid URL]'; }
  }

  function beforeSend(event) {
    // No profile data, form state, storage, breadcrumbs or arbitrary contexts.
    delete event.user;
    delete event.extra;
    delete event.breadcrumbs;
    delete event.contexts;
    event.request = {url: location.origin + location.pathname};
    for (const value of event.exception && event.exception.values || []) {
      for (const frame of value.stacktrace && value.stacktrace.frames || []) {
        frame.filename = cleanUrl(frame.filename);
        delete frame.vars;
      }
    }
    return event;
  }

  window.addEventListener('error', earlyError);
  window.addEventListener('unhandledrejection', earlyRejection);

  const script = document.createElement('script');
  script.src = SDK_URL;
  script.integrity = SDK_INTEGRITY;
  script.crossOrigin = 'anonymous';
  script.referrerPolicy = 'no-referrer';
  script.async = true;
  script.fetchPriority = 'low';
  script.onerror = fail;
  script.onload = function () {
    try {
      const sentry = window.Sentry;
      sentry.init({
        dsn: DSN,
        environment: options.environment || (local ? 'development' : 'production'),
        defaultIntegrations: false,
        integrations: [
          sentry.globalHandlersIntegration(),
          sentry.browserApiErrorsIntegration(),
          sentry.eventFiltersIntegration(),
          sentry.dedupeIntegration()
        ],
        dataCollection: {
          userInfo: false, cookies: false, httpHeaders: false, httpBodies: [],
          urlQueryParams: false, stackFrameVariables: false
        },
        maxBreadcrumbs: 0,
        sendClientReports: false,
        beforeSend,
        initialScope: {tags: {app: 'halocosplay-frontend'}}
      });
      sdk = sentry;
      stopBuffering();
      for (const item of pending.splice(0)) {
        captureException(item.error, item.operation, item.mechanism);
      }
    } catch (_) { fail(); }
  };
  document.head.appendChild(script);
}());
