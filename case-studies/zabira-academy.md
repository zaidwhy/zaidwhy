# Case study: shipping into a live product

**27 merged pull requests into a production learning platform over twelve days. Payments,
security hardening, an end-to-end test suite with a CI gate, and a sitewide search feature
built from nothing to voice input.**

Every change reviewed and merged by the repository owner. The codebase is private, which is
why this document exists - the work is real and the commits are not public, so here is an
account of it with enough specifics to check.

**Disclosure up front:** the platform belongs to a family member's business. It is a real
company with real customers taking real payments, and every pull request went through review
before merge, but I would rather say whose product it is than have someone discover it later.

---

## What it is

An Islamic education platform - courses, a media library, an online store, events, and a
kids' section - built on a PHP backend with a Next.js front end. Live, transacting, with
paying customers and a launch deadline.

I joined as an outside contributor. I did not design the system, and most of what follows is
the ordinary and unglamorous work of making something someone else built survive contact
with the public.

---

## The security pass

The most consequential stretch. A live product that takes payments and stores customer data
had a set of vulnerabilities that were individually small and collectively serious.

**Raw exception text was leaking to clients on server errors** - stack traces, file paths,
and query fragments returned to the browser on failure. Fixed across 226 files in one pass,
because a partial fix here is not a fix: the one endpoint you miss is the one that gets
found.

**Sixty mutating endpoints had no Origin check.** Any page on any domain could issue state
changing requests against them on behalf of a logged-in user. Added explicit Origin
validation plus request-method guards across all sixty.

**An HTML sanitizer bypass** in the rich-text rendering used by the events module, closed and
backed with DOMPurify.

Alongside those: session revocation, rate limiting on public forms, CORS reflection, path
containment on file handling, login throttling with the attempt counter surfaced in the UI so
a locked-out user is told what is happening rather than left guessing, and scrubbing example
passwords out of a committed environment file.

Also, quietly, **34 customer uploads that had been committed to git** - gallery and library
media that belonged in storage, not in version control. Confirmed safe, then untracked, with
the ignore rules fixed so it could not recur.

---

## The bug that was hiding behind a green feature

My favourite piece of work here found nothing wrong with what I was building.

I shipped voice search and CI came back red. The obvious conclusion was that I had broken
something. I had not - and confirming that took the actual investigation.

Bisecting `gh run list --branch main` showed CI had been failing on **every push since a
commit three days before I touched the repository**. That commit added letters-only
validation to the registration first-name field. The end-to-end suite's fixture name was
`'E2E'`, which contains a digit. So registration failed client-side validation silently -
no thrown error, just a toast and no navigation - and the test sat waiting for a URL change
until it timed out twenty seconds later. The failure message pointed at a timeout, which
pointed nowhere near the cause.

Confirmed by downloading the failed run's Playwright report artifact and reading the
error-context snapshot, which showed the First Name field marked invalid with the validation
message visible at the exact moment of failure.

Fixed the fixture (`'E2E'` to `'Ezee'`) and shipped it as **its own pull request**, separate
from the feature branch, rather than folding an unrelated repair into a feature PR and
muddying both. The feature branch was then rebased on top.

A smaller trap surfaced during the same investigation and is worth recording: my local
`node_modules` had drifted from `package-lock.json`, and the resulting `tsc` "cannot find
module" errors looked exactly like real type errors. Ruling that out before trusting local
output against CI was the difference between diagnosing the problem and chasing a ghost.

---

## Testing and the CI gate

Before this, nothing stopped a broken build from merging.

I built an **end-to-end suite covering the seven launch-critical flows** - the paths where
failure costs money or trust - and wired it to a CI gate so those flows are exercised on
every push.

Making that run in CI meant standing up a portable PHP and MariaDB stack on the runner, which
had its own set of small hostile details: the schema file hardcoded its own database name, the
MariaDB client had to be installed separately on the runner image, and `NODE_ENV` needed
job-level rather than step-level scope. None of that is interesting individually. Together it
is the difference between a test suite that exists and one that runs.

---

## Building a feature end to end

The last stretch was product work rather than repair: sitewide search, built in five stages
over five days.

1. A public, read-only, **fail-soft search backend** - if search breaks, the page still loads.
2. A **homepage dropdown** with grouped live results, in the style of a property-search site.
3. **Per-page live suggestions** on every section-level search bar.
4. Then a discovery that reframed the rest: **the homepage hero search box was decorative.**
   It had been shipped as a styled input wired to nothing at all. Someone typing into the most
   prominent control on the front page got silence. Wired it to the backend built in stage one.
5. **Voice search** across the global modal and every per-page bar, using the browser's Web
   Speech API and feature-detected client-side, so the microphone button simply does not render
   where it is unsupported rather than appearing and failing.

Before building stage five I confirmed which surfaces it should cover and whether it should
search automatically on transcription or wait for confirmation, rather than guessing and
building the wrong one.

---

## Also shipped

- Fixed a **cancelled-payment bug** and added free-trial validation.
- Rebuilt the **invoice PDF and HTML template** - compact, on-brand, and three rendering bugs
  gone - plus the invoice wrapper, payment-success and order pages to match.
- Fixed **invoice emails**, removing a raw-HTML attachment fallback and a dead invoice link.
- Repaired **editing and deleting sitewide**, broken by the previous week's method guards.
- Fixed store currency display, description rendering, and admin bugs.
- Fixed **Kids Corner Memory Match** reshuffling its tiles on every tap.
- An **accessibility pass**, store uploads, kids copy, and completion sharing for launch.

---

## The numbers

| | |
|---|---|
| Merged pull requests | **27** |
| Span | 12 days (2026-08-12 to 2026-08-24) |
| Lines added / removed | +8,838 / -1,619 |
| File changes | 557 |
| Largest single PR | 1,914 lines (P0 launch blockers) |
| Rejected or abandoned | 0 |

---

## Why this is the strongest thing in my portfolio

Everything else I have built, I also specified, reviewed and merged. Here I did none of those
things. I worked inside someone else's architecture, to someone else's priorities and
deadline, and every change had to pass their review before it reached customers.

That constraint is the whole point. It is where you find out whether you can read an unfamiliar
codebase quickly, scope a change so it can actually be reviewed, keep an unrelated fix out of a
feature branch, and tell the difference between the bug you were sent to fix and the one that
was already there.

It is also the closest thing in my portfolio to the actual job.
