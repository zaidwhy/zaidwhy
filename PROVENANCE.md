# Provenance

This repository is the GitHub profile of **Zaid Ali Syed** ([@zaidwhy](https://github.com/zaidwhy)).

Everything on the profile page - the writing, the artwork, the research results - is original work. This file exists so that authorship can be checked rather than assumed.

## Identity

```
Zaid Ali Syed
ORCID    0009-0003-4313-1510   https://orcid.org/0009-0003-4313-1510
ed25519  EFE9 4832 B2B9 80D9 B583  91F2 8FAA BCC1 B1AC 09E5
```

The ORCID iD is a permanent identifier bound to me personally and is the authoritative record of what I have authored. The signing key below covers everything in these repositories.

The public key is in this repository as [`zaid-pubkey.txt`](zaid-pubkey.txt).

## What is signed

- **Commits.** Every commit made on this account is signed with the key above. GitHub shows them as *Verified*. A commit in my name without a valid signature was not made by me.
- **This statement.** [`PROVENANCE.sig.txt`](PROVENANCE.sig.txt) is a clear-signed authorship assertion covering the artwork and research listed in it.

## How to verify

```bash
# Import the key and check the fingerprint matches the one above.
gpg --import zaid-pubkey.txt
gpg --fingerprint zaidsyed7021@gmail.com

# Verify the signed authorship statement.
gpg --verify PROVENANCE.sig.txt

# Verify commit signatures on any of my repositories.
git clone https://github.com/zaidwhy/augur && cd augur
git log --show-signature -3
```

## On the artwork

The SVG files in [`assets/`](assets/) are hand-authored, not produced by a badge or stats service. Each one carries an authorship manifest in its source, including the fingerprint above. They are served from this repository, so if you find them rendering on a page that is not mine, they are being loaded from here.

## On the research

The findings referenced on the profile page live in their own repositories with raw data and reproduction scripts:

- [COLD READ](https://github.com/zaidwhy/coldread) - the anonymity half-life belongs to the reader
- [AUGUR](https://github.com/zaidwhy/augur) - the effective epistemic date of time-locked language models

Both are archived with a permanent DOI and carry `CITATION.cff`. Cite those records rather than a copy.

## Reuse

The code in my repositories is MIT licensed - use it, with the copyright notice retained as the licence requires. The prose and artwork on this profile are not part of that grant: **(c) 2026 Zaid Ali Syed, all rights reserved.**

If you want to build a profile like this one, take the idea, not the file. The idea is the interesting part anyway: make every claim link to the artifact that proves it.
