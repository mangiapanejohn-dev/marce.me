import type { APIRoute } from "astro";

const getRobotsTxt = (sitemapURL: URL) => `
User-agent: *
Allow: /
Disallow: /ø
Disallow: /%C3%B8
Disallow: /zh/ø
Disallow: /zh/%C3%B8
Disallow: /ƒ
Disallow: /%C6%92
Disallow: /zh/ƒ
Disallow: /zh/%C6%92

Sitemap: ${sitemapURL.href}
`;

export const GET: APIRoute = ({ site }) => {
  const sitemapURL = new URL("sitemap-index.xml", site);
  return new Response(getRobotsTxt(sitemapURL));
};
