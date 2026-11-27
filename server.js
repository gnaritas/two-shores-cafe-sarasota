const { createServer } = require("http");
const { readFileSync } = require("fs");
const { join, extname } = require("path");

const PORT = process.env.PORT || 3000;
const PUB = join(__dirname, "public");
const SITE = "Two Shores Café";
const EMAIL_RE = /^[^\s@]+@[^\s@,;]+$/;

const MIME = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".svg": "image/svg+xml",
  ".png": "image/png", ".jpg": "image/jpeg", ".gif": "image/gif",
  ".ico": "image/x-icon", ".xml": "application/xml; charset=utf-8", ".txt": "text/plain; charset=utf-8",
};

function readBody(req, limit = 20000) {
  return new Promise((resolve, reject) => {
    let size = 0; const chunks = [];
    req.on("data", (c) => {
      size += c.length;
      if (size > limit) { reject(new Error("body too large")); req.destroy(); return; }
      chunks.push(c);
    });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

function decodeForm(raw) {
  const o = {};
  for (const part of raw.split("&")) {
    if (!part) continue;
    const i = part.indexOf("=");
    const k = decodeURIComponent(part.slice(0, i < 0 ? part.length : i).replace(/\+/g, " "));
    const v = i < 0 ? "" : decodeURIComponent(part.slice(i + 1).replace(/\+/g, " "));
    if (!(k in o)) o[k] = v;
  }
  return o;
}

const clean = (s, max) => String(s || "").replace(/[\r\n]+/g, " ").replace(/[<>]/g, "").trim().slice(0, max);

function send(res, code, body, type, extra) {
  const headers = { "Content-Type": type, "Content-Length": Buffer.byteLength(body), "X-Robots-Tag": "noindex, nofollow" };
  for (const [k, v] of Object.entries(extra || {})) headers[k] = v;
  res.writeHead(code, headers);
  res.end(body);
}

function serveStatic(req, res, pathname) {
  let rel = pathname === "/" ? "/index.html" : pathname;
  if (!/\.[a-z0-9]+$/i.test(rel)) rel += ".html";
  let file;
  try { file = readFileSync(join(PUB, rel)); }
  catch { try { file = readFileSync(join(PUB, "404.html")); rel = "/404.html"; } catch { return send(res, 404, "not found", "text/plain"); } }
  const code = rel.endsWith("404.html") && pathname !== "/404" ? 404 : 200;
  send(res, code, file, MIME[extname(rel).toLowerCase()] || "application/octet-stream");
}

async function formError(res, msg) {
  console.log("CONTACTREJECT", msg);
  const body = `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>Message not sent — ${SITE}</title></head><body style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;background:#0a2c37;color:#e9f1f2;display:grid;place-items:center;min-height:100vh;margin:0"><main style="max-width:520px;padding:40px 26px;background:#10404d;border:1px solid #c9d7db;border-radius:16px;text-align:center"><h1 style="font-size:26px;margin:0 0 12px">Message not sent</h1><p style="margin:0 0 18px">${msg}</p><p style="margin:0">Please <a href="/contact" style="color:#d18a3a;font-weight:600">try again</a> or call the shop.</p></main></body></html>`;
  send(res, 400, body, "text/html; charset=utf-8");
}

async function handleContact(req, res) {
  let raw;
  try { raw = await readBody(req); }
  catch { return formError(res, "That message was too long or didn't arrive."); }
  const f = decodeForm(raw);
  const name = clean(f.name, 120), phone = clean(f.phone, 40), email = clean(f.email, 160), message = clean(f.message, 2000);
  if (!name || !message) return formError(res, "Please add your name and a message.");
  if (email && !EMAIL_RE.test(email)) return formError(res, "That email address doesn't look right.");
  const key = process.env.BREVO_API_KEY || "";
  const alias = process.env.MAIL_ALIAS || "jarvis+websites@onsmalltalk.com";
  const toEmail = process.env.MAIL_TO || "jarvis+websites@onsmalltalk.com";
  const toName = process.env.MAIL_TO_NAME || SITE;
  if (!key) return formError(res, "The message form isn't configured on this server yet — please try again shortly.");
  const origin = `https://${(req.headers.host || "").split(":")[0]}`;
  const text = [
    `From: ${name}${phone ? " (" + phone + ")" : ""} <${email || "not given"}>`,
    "", message, "",
    `Sent via the ${SITE} contact form`, "Reply-To: " + alias,
    "IP: " + ((req.socket && req.socket.remoteAddress) || "?"),
  ].join("\n");
  const html = `<p><b>From:</b> ${name}${phone ? " (" + phone + ")" : ""} &lt;${email || "not given"}&gt;</p>` +
    `<p>${message.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")}</p>` +
    `<hr><p>Sent via the <a href="${origin}/contact">${SITE} contact form</a>.<br>Reply-To: ${alias}<br>IP: ${req.socket ? req.socket.remoteAddress : "?"}</p>`;
  try {
    const r = await fetch("https://api.brevo.com/v3/smtp/email", {
      method: "POST",
      headers: { "api-key": key, "content-type": "application/json", "accept": "application/json" },
      body: JSON.stringify({
        sender: { name: SITE, email: alias },
        to: [{ email: toEmail, name: toName }],
        replyTo: { email: alias, name: SITE },
        subject: `[Two Shores Café] website contact from ${name}`,
        textContent: text, htmlContent: html,
      }),
    });
    const bodyTxt = await r.text();
    if (!r.ok) { console.log("MAILERR", r.status, bodyTxt.slice(0, 300)); return formError(res, "We couldn't deliver your message just now — please try again in a moment."); }
    console.log("MAILSENT", r.status, (JSON.parse(bodyTxt).messageId || ""));
  } catch (e) {
    console.log("MAILERR", e.message);
    return formError(res, "We couldn't deliver your message just now — please try again in a moment, or call the shop.");
  }
  res.writeHead(303, { Location: "/thanks", "X-Robots-Tag": "noindex, nofollow" });
  res.end();
}

createServer(async (req, res) => {
  let pathname;
  try { pathname = decodeURIComponent(new URL(req.url, "http://x").pathname); }
  catch { return serveStatic(req, res, "/404"); }
  if (req.method === "GET" && pathname === "/healthz") return send(res, 200, JSON.stringify({ ok: true }), "application/json");
  if (req.method === "GET" && pathname === "/open") {
    let gif;
    try { gif = readFileSync(join(PUB, "pixel.gif")); }
    catch { return send(res, 404, "no pixel", "text/plain"); }
    const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || (req.socket && req.socket.remoteAddress) || "";
    console.log("OPEN", (req.query && req.query.t) || "none", ip);
    res.writeHead(200, {
      "Content-Type": "image/gif", "Content-Length": gif.length,
      "Cache-Control": "no-store, no-cache, no-cache=Set-Cookie, private, max-age=0",
      Expires: "0", Pragma: "no-cache", "X-Robots-Tag": "noindex, nofollow",
    });
    return res.end(gif);
  }
  if (req.method === "POST" && pathname === "/contact") return handleContact(req, res);
  if (req.method !== "GET" && req.method !== "HEAD") return send(res, 405, "method not allowed", "text/plain");
  serveStatic(req, res, pathname);
}).listen(PORT, () => console.log(`Two Shores site on :${PORT}`));
