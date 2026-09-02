export const SITE = {
  website: "https://marcyy.me/",
  author: "@marcE",
  profile: "https://marcyy.me/",
  desc: "Building MØBIUS, an experimental agent runtime, plus the developer tools and systems around it. Notes on architecture, security, and what breaks when software meets real people.",
  title: "MarcEllington.me",
  ogImage: "", // empty → falls back to dynamic /og.png (branded with site title)
  lightAndDarkMode: true,
  postPerIndex: 4,
  postPerPage: 4,
  scheduledPostMargin: 0,
  showArchives: true,
  showBackButton: true, // show back button in post detail
  editPost: {
    enabled: false,
    text: "Edit page",
    url: "https://github.com/",
  },
  dynamicOgImage: true,
  dir: "ltr", // "rtl" | "auto"
  lang: "en", // html lang code. Set this empty and default will be "en"
  timezone: "Asia/Shanghai", // Default global timezone (IANA format)
} as const;