import { getCollection } from "astro:content";

export function getLangFromUrl(url: URL): string {
  const [, lang] = url.pathname.split("/");
  if (lang === "zh") return "zh";
  return "en";
}

export const translations = {
  en: {
    home: "Home",
    blog: "Blog",
    about: "About",
    posts: "Posts",
    tags: "Tags",
    search: "Search"
  },
  zh: {
    home: "首页",
    blog: "博客",
    about: "关于",
    posts: "文章",
    tags: "标签",
    search: "搜索"
  }
};

export function useTranslations(lang: string) {
  return translations[lang as keyof typeof translations] || translations.en;
}