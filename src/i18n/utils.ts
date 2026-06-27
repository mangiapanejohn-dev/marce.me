import { ui, defaultLang, type Lang } from "./ui";

/** Read the active language from the first URL path segment (`/zh/...` → zh). */
export function getLangFromUrl(url: URL): Lang {
  const [, seg] = url.pathname.split("/");
  return seg === "zh" ? "zh" : "en";
}

/** Translation helper, falls back to the default language for missing keys. */
export function useTranslations(lang: Lang) {
  return function t(key: keyof (typeof ui)[typeof defaultLang]): string {
    return ui[lang][key] || ui[defaultLang][key];
  };
}

/** Strip a leading `/zh` so the path is always English-rooted. */
function stripLangPrefix(path: string): string {
  if (path === "/zh") return "/";
  if (path.startsWith("/zh/")) return path.slice(3);
  return path;
}

/**
 * Map any internal path to its equivalent in `lang`.
 * `/posts` → `/zh/posts` (zh) and `/zh/posts` → `/posts` (en). `/` ↔ `/zh`.
 */
export function localizePath(path: string, lang: Lang): string {
  const base = stripLangPrefix(path) || "/";
  if (lang === "en") return base;
  return base === "/" ? "/zh" : `/zh${base}`;
}

/** Pair an English post with its Chinese version: `foo.md` and `foo.zh.md`
 *  share the key `foo` (glob loader ids are extension-less, so id is `foo.zh`). */
export function getTranslationKey(id: string): string {
  return id.replace(/\.zh$/, "");
}
