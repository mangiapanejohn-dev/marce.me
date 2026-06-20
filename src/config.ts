export const SITE = {
  website: "https://marce.me/",
  author: "@marcE",
  profile: "https://marce.me/",
  desc: "Vibe Coder. Building AI tools that actually remember you. Resonix-AG and RE CODE — every commit lands on GitHub for you to fork & remix.",
  title: "MarkEllington.me",
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