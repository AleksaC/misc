// ==UserScript==
// @match *://*/*
// ==/UserScript==

const REDIRECTS = [
  {
    urlPattern: "https?://circleci.com/?$",
    target: "https://app.circleci.com",
  },
  {
    urlPattern: "https?://discord.com/?$",
    target: "https://discord.com/app",
  },
  {
    urlPattern: "https?://aws.amazon.com/?$",
    target: "https://console.aws.amazon.com",
  },
  {
    urlPattern: "https?://(www.)?netlify.com/?$",
    target: "https://app.netlify.com",
  },
  {
    urlPattern: "https?://(www.)?bitwarden.com/?$",
    target: "https://vault.bitwarden.com",
  },
  {
    urlPattern: "https?://(www.)?cloudflare.com/?$",
    target: "https://dash.cloudflare.com",
  },
];

for (const redirect of REDIRECTS) {
  const pattern = new RegExp(redirect.urlPattern);
  if (pattern.test(window.location.href)) {
    window.location = redirect.target;
  }
}
