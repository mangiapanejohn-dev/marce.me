/**
 * The "Stay Connected" form on /about and /zh/about.
 *
 * A visitor leaves a name and an email; this sends them to Marc's inbox through Resend, with the
 * visitor as Reply-To so answering is one click. It replaced a `mailto:` form, which only opened the
 * visitor's own mail app and usually sent nothing.
 *
 * Works with and without JavaScript: the page's script posts with `Accept: application/json` and
 * shows the result in place; a plain form post is redirected back to the page, to an anchor that
 * shows the same result.
 *
 * Env: RESEND_API_KEY (from the Vercel ↔ Resend integration). NEWSLETTER_TO overrides the inbox;
 * until a sending domain is verified in Resend, it must be the Resend account's own address.
 */

const TO = process.env.NEWSLETTER_TO || "mangiapanejohn@icloud.com";
const FROM = process.env.NEWSLETTER_FROM || "marc.me <onboarding@resend.dev>";
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

type Result = { ok: boolean; error?: "invalid" | "failed" };

export async function POST(request: Request): Promise<Response> {
  const wantsJson = (request.headers.get("accept") ?? "").includes("application/json");

  let form: FormData;
  try {
    form = await request.formData();
  } catch {
    return reply({ ok: false, error: "invalid" }, "en", wantsJson, 400);
  }

  const lang = form.get("lang") === "zh" ? "zh" : "en";
  const name = String(form.get("name") ?? "").trim().slice(0, 100);
  const email = String(form.get("email") ?? "").trim();

  // A field people never see; anything in it came from a bot. Say yes and send nothing.
  if (String(form.get("website") ?? "") !== "") {
    return reply({ ok: true }, lang, wantsJson);
  }
  if (email.length > 254 || !EMAIL.test(email)) {
    return reply({ ok: false, error: "invalid" }, lang, wantsJson, 400);
  }

  const key = process.env.RESEND_API_KEY;
  if (!key) {
    console.error("subscribe: RESEND_API_KEY is not set");
    return reply({ ok: false, error: "failed" }, lang, wantsJson, 500);
  }

  const who = name ? `${name} <${email}>` : email;
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: FROM,
      to: [TO],
      reply_to: email,
      subject: `New subscriber: ${name || email}`,
      text: [
        `${who} signed up on marc.me (${lang === "zh" ? "中文" : "English"} About page).`,
        "",
        "Reply to this email to write back to them.",
      ].join("\n"),
    }),
  });

  if (!res.ok) {
    console.error("subscribe: Resend", res.status, (await res.text()).slice(0, 300));
    return reply({ ok: false, error: "failed" }, lang, wantsJson, 502);
  }
  return reply({ ok: true }, lang, wantsJson);
}

function reply(result: Result, lang: "en" | "zh", json: boolean, status = 200): Response {
  if (json) {
    return new Response(JSON.stringify(result), {
      status,
      headers: { "Content-Type": "application/json" },
    });
  }
  // No script on the page: go back to it, to the anchor that shows the outcome.
  const page = lang === "zh" ? "/zh/about" : "/about";
  const anchor = result.ok ? "subscribed" : "subscribe-failed";
  return new Response(null, { status: 303, headers: { Location: `${page}#${anchor}` } });
}
