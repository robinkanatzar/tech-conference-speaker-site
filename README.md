# Tech Conference Speaker — website

The whole site for https://techconferencespeaker.com, served by GitHub Pages from `main`. It is a mentoring exchange for iOS developers who want to speak at developer conferences. The design follows zerotoaccessible.com (`zero-to-accessible-site` repo).

Plain HTML, no build step. Every page uses `styles.css` and `fonts/`.

| Page | Path | What's there |
|---|---|---|
| Home | `/` | hero, three entry points, how it works, what a mentor helps with, questions, Robin |
| Get a mentor | `/speakers/` | form for speakers: talk idea, talk, conference |
| Be a mentor | `/mentors/` | form for volunteer mentors |
| For conferences | `/conferences/` | form for organizers who want a mentoring or diversity program |
| About | `/about/` | Robin, the Tech Talks book, contact links |

## How the forms work

Nothing is sent to a server and nothing is stored. Each form builds an email to hello@robinkanatzar.com: `assets/form.js` collects the answers, opens the visitor's email app with them filled in, and shows the same text on the page to copy in case no email app opens. Without JavaScript the form's `action` is a plain `mailto:` link.

- The email's subject is the form's `data-subject`.
- Each question is an element with `data-q` (the line that appears in the email above the answer). To add a question, copy a `field` block and give its input a new `id` and `name`.
- To change the address, edit `EMAIL` in `tools/site.py`, the `data-mailto` and `action` of each form, and the links in the pages.

## Shared header and footer

Edit `TABS` or `FOOTER` in `tools/site.py`, then run `python3 tools/site.py`. It rewrites the header and footer of every page and marks the current tab. Page content is never touched.

## Files

- `CNAME`: custom domain for GitHub Pages
- `.nojekyll`: serve the files as they are
- `assets/mic.svg`: the logo (white on transparent, used as a CSS mask so it follows light and dark mode)
- `fonts/`: Atkinson Hyperlegible Next (SIL Open Font License, see `fonts/OFL.txt`)

## Accessibility notes

Built against WCAG 2.2 AA: text contrast at least 7:1 on the page background in light and dark mode, the current tab is marked with `aria-current="page"` (not just its bar), lists without bullets carry `role="list"`, every form field has a visible label and hints are tied to it with `aria-describedby`, radio and checkbox groups are `fieldset`s with a `legend`, every button and choice is at least 44 px tall, focus is a 3 px ring in the accent colour, and after a form is submitted focus moves to the result. Forced-colors, `prefers-contrast: more` and reduced motion are handled in the stylesheet. No cookies, no trackers, no third-party scripts.

## DNS for GitHub Pages

At the registrar: `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, and a `CNAME` for `www` → `robinkanatzar.github.io`. When GitHub shows the certificate is ready, tick **Enforce HTTPS** in Settings → Pages.
