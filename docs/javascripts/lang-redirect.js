// Browser-language auto-detect for the static site.
// GitHub Pages can't negotiate Accept-Language, so on first visit to an English
// page we redirect French-preferring browsers to the /fr/ equivalent. We set a
// flag once a user picks a language so we never fight a deliberate choice.
(function () {
  try {
    if (localStorage.getItem("lang-pref")) return;           // user already chose
    var path = location.pathname;
    if (/(^|\/)fr\//.test(path)) return;                     // already on French

    var prefersFr = (navigator.languages || [navigator.language || ""])
      .some(function (l) { return l.toLowerCase().indexOf("fr") === 0; });
    if (!prefersFr) return;

    // Determine the site base. On GitHub Pages project sites the base is
    // "/<repo>/"; on a user/custom domain it's "/".
    var base = "/";
    if (location.hostname.endsWith("github.io")) {
      var first = path.split("/").filter(Boolean)[0];
      if (first) base = "/" + first + "/";
    }
    var rest = path.indexOf(base) === 0 ? path.slice(base.length) : path.replace(/^\//, "");
    location.replace(base + "fr/" + rest);
  } catch (e) { /* never block the page on a redirect attempt */ }
})();

// Record an explicit language choice (clicking the selector / a /fr/ link) so the
// auto-redirect above stays out of the user's way afterward.
document.addEventListener("click", function (e) {
  var a = e.target.closest && e.target.closest("a");
  if (!a) return;
  var href = a.getAttribute("href") || "";
  if (/(^|\/)fr\//.test(href) || a.hreflang === "fr") localStorage.setItem("lang-pref", "fr");
  else if (a.hreflang === "en") localStorage.setItem("lang-pref", "en");
});
