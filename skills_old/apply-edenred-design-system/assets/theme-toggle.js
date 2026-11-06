/* ============================================================
   assets/theme-toggle.js — Edenred Design System · Theme toggle
   ------------------------------------------------------------
   ROLE  Generic dark/light theme utility for EdenChat apps.
         Toggles [data-theme] on <html>, persists the choice, and
         updates the SVG icon (moon/sun) via <use href> swap.
   USE   1. Load edenred-theme.css (defines [data-theme="dark"]).
         2. Paste icons.html sprite once (needs #ic-moon, #ic-sun).
         3. Add a toggle button whose <use> starts on #ic-moon:
            <button id="themeToggle" class="eds-btn eds-btn-ghost"
                    aria-label="Basculer le thème" aria-pressed="false">
              <svg class="eds-icon" id="themeIcon" aria-hidden="true">
                <use href="#ic-moon"/>
              </svg>
            </button>
         4. Include this script (defer). initTheme() runs on load.
   NOTES
     - No emoji: the icon is a real SVG symbol, swapped by href.
     - Respects OS preference on first visit (no stored choice).
     - Sandbox-safe: uses localStorage guarded in try/catch (some
       srcdoc iframes restrict storage).
   ============================================================ */

(function () {
  "use strict";

  var STORAGE_KEY = "eds-theme";        // "light" | "dark"
  var TOGGLE_ID   = "themeToggle";
  var ICON_ID     = "themeIcon";

  /* --- storage helpers (guarded for sandboxed iframes) --- */
  function readStored() {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }
  function writeStored(v) {
    try { localStorage.setItem(STORAGE_KEY, v); } catch (e) { /* no-op */ }
  }

  /* --- resolve the theme to apply on load --- */
  function resolveInitialTheme() {
    var stored = readStored();
    if (stored === "light" || stored === "dark") return stored;
    // no explicit choice → follow OS preference
    var prefersDark = window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;
    return prefersDark ? "dark" : "light";
  }

  /* --- swap the SVG icon (moon in light mode → tap for dark, etc.) --- */
  function updateIcon(theme) {
    var icon = document.getElementById(ICON_ID);
    if (!icon) return;
    var use = icon.querySelector("use");
    if (!use) return;
    // show the icon representing the action available:
    // in dark mode show sun (tap → go light); in light show moon.
    var href = theme === "dark" ? "#ic-sun" : "#ic-moon";
    // support both href and legacy xlink:href
    use.setAttribute("href", href);
    use.setAttributeNS("http://www.w3.org/1999/xlink", "xlink:href", href);
  }

  /* --- apply a theme to the document --- */
  function applyTheme(theme, persist) {
    document.documentElement.setAttribute("data-theme", theme);
    updateIcon(theme);
    var btn = document.getElementById(TOGGLE_ID);
    if (btn) {
      btn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
      btn.setAttribute("aria-label",
        theme === "dark" ? "Passer en thème clair" : "Passer en thème sombre");
    }
    if (persist) writeStored(theme);
  }

  /* --- public: toggle between light and dark --- */
  function toggleTheme() {
    var current = document.documentElement.getAttribute("data-theme") || resolveInitialTheme();
    applyTheme(current === "dark" ? "light" : "dark", true);
  }

  /* --- init on load --- */
  function initTheme() {
    applyTheme(resolveInitialTheme(), false);
    var btn = document.getElementById(TOGGLE_ID);
    if (btn) btn.addEventListener("click", toggleTheme);

    // live-follow OS changes only while the user hasn't chosen explicitly
    if (window.matchMedia) {
      var mq = window.matchMedia("(prefers-color-scheme: dark)");
      var onChange = function (e) {
        if (!readStored()) applyTheme(e.matches ? "dark" : "light", false);
      };
      if (mq.addEventListener) mq.addEventListener("change", onChange);
      else if (mq.addListener) mq.addListener(onChange); // older engines
    }
  }

  // expose for manual calls (e.g. a custom button elsewhere)
  window.toggleTheme = toggleTheme;
  window.setTheme = function (t) { if (t === "light" || t === "dark") applyTheme(t, true); };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initTheme);
  } else {
    initTheme();
  }
})();