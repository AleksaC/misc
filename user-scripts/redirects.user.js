// ==UserScript==
// @match *://*/*
// ==/UserScript==

const REDIRECTS = [
  {
    urlPattern: "https?://circleci.com/?",
    target: "https://app.circleci.com",
  },
  {
    urlPattern: "https?://discord.com/?",
    target: "https://discord.com/app",
  },
  {
    urlPattern: "https?://aws.amazon.com/?",
    target: "https://console.aws.amazon.com",
  },
];

for (const redirect of REDIRECTS) {
  const pattern = new RegExp(redirect.urlPattern);
  if (pattern.test(window.location.href)) {
    window.location = redirect.target;
  }
}
