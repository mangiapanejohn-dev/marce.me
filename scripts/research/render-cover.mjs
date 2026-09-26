// Rasterise a cover SVG with the site's resvg: node scripts/research/render-cover.mjs <in.svg> <out.png> [font.ttf ...]
// System fonts supply the serif and sans; pass the Google Sans Code files explicitly (the site loads it from
// Google Fonts, so it is not installed). sharp then writes the webp cover from the PNG.
import { Resvg } from "@resvg/resvg-js";
import fs from "node:fs";

const [src, out, ...fontFiles] = process.argv.slice(2);
const png = new Resvg(fs.readFileSync(src, "utf8"), {
  fitTo: { mode: "width", value: 1200 },
  font: { loadSystemFonts: true, fontFiles, defaultFontFamily: "Avenir Next" },
}).render().asPng();
fs.writeFileSync(out, png);
console.log(out, png.length);
