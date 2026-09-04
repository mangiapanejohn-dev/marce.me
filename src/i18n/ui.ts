// Central source for all translatable UI strings (site chrome).
// Page-specific titles/descriptions live inline in each page; this file
// only holds strings used by shared components (Header, Footer, Breadcrumb,
// Pagination, PostDetails, Datetime, LanguagePicker).

export const languages = {
  en: "English",
  zh: "中文",
} as const;

export type Lang = keyof typeof languages;

export const defaultLang: Lang = "en";

export const ui = {
  en: {
    "nav.posts": "Posts",
    "nav.tags": "Tags",
    "nav.categories": "Categories",
    "nav.about": "About",
    "nav.archives": "Archives",
    "nav.search": "Search",
    skip: "Skip to content",
    "menu.open": "Open Menu",
    "menu.close": "Close Menu",
    "footer.copyright": "Copyright ©",
    "footer.rights": "All rights reserved.",
    "pagination.prev": "Prev",
    "pagination.next": "Next",
    "post.goBack": "Go back",
    "post.previous": "Previous Post",
    "post.next": "Next Post",
    "post.updated": "Updated:",
    "post.share": "Share this post on:",
    "post.fallback":
      "This post isn't available in Chinese yet — showing the English original.",
    "breadcrumb.home": "Home",
    "lang.toggle": "切换语言",
  },
  zh: {
    "nav.posts": "文章",
    "nav.tags": "标签",
    "nav.categories": "分类",
    "nav.about": "关于",
    "nav.archives": "归档",
    "nav.search": "搜索",
    skip: "跳到主要内容",
    "menu.open": "打开菜单",
    "menu.close": "关闭菜单",
    "footer.copyright": "版权所有 ©",
    "footer.rights": "保留所有权利。",
    "pagination.prev": "上一页",
    "pagination.next": "下一页",
    "post.goBack": "返回",
    "post.previous": "上一篇",
    "post.next": "下一篇",
    "post.updated": "更新于:",
    "post.share": "分享到:",
    "post.fallback": "本文暂无中文版,以下为英文原文。",
    "breadcrumb.home": "首页",
    "lang.toggle": "Switch language",
  },
} as const;
