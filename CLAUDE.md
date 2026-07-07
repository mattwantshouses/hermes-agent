# Local branch policy — read before any git action in this repo

This checkout is `mattwantshouses/hermes-agent`, which NousResearch's own
team pushes to directly (teknium1, Fan Yang, helix4u, and others commit
straight to `origin/main` here — it is effectively a live mirror of their
upstream, not a normal fork you control the pace of).

**Rules:**

1. **Never commit directly to `main`.** `main` must always stay an exact,
   untouched mirror of `origin/main` (0 ahead / 0 behind) so a plain
   `git pull` on it is always a trivial fast-forward. Committing here
   recreates the exact confusion resolved on 2026-07-07 (a shallow clone
   plus a stray local commit made `main` look "2 ahead, 1 behind" when it
   was really 305 commits behind with a redundant duplicate fix on top).
2. **All local work (fixes, experiments, anything you'd `git commit`)
   goes on `matt/cua-timeout-reconnect-fix`**, or a new branch created off
   the current `main` if that one has grown stale. This repo is normally
   left checked out on that branch, not `main`, specifically so a fresh
   session lands in the right place by default. If you find yourself on
   `main` with changes to commit, stop and switch branches first:
   `git checkout matt/cua-timeout-reconnect-fix` (or create a new
   `matt/<topic>` branch from current `main`).
3. **Do not run `git reset --hard`, `git rebase` onto `main`, or `git pull`
   with `--rebase` without explicit confirmation from Matt first** — these
   are exactly the operations that can silently discard local commits or
   blend in upstream churn you haven't reviewed.
4. **To bring in newer upstream code:** fetch `origin/main`, then rebase
   `matt/cua-timeout-reconnect-fix` (or whichever patch branch is active)
   onto the updated `main`, run the test suite, and only then consider
   pointing the running gateway at it. Never fast-forward `main` itself
   past `origin/main` in a way that leaves local commits stranded on it —
   `main` should only ever move via a clean fetch that keeps it identical
   to `origin/main`.

This file is tracked **only on `matt/cua-timeout-reconnect-fix`** (and
future `matt/<topic>` branches) — never on `main`. That keeps it syncing
normally across machines via `git push`/`git pull` on this branch while
`main` stays byte-identical to `origin/main` with zero local commits.
It will not exist when `main` is checked out (that's expected — the
in-repo instructions only need to be visible from the branch you're
actually meant to work on).

See also `AGENTS.md` (upstream-owned; its top has a short pointer back
to this file for Codex, added as a commit **only on
`matt/cua-timeout-reconnect-fix`**, same as this file — not on `main`,
so `main` still tracks `origin/main`'s `AGENTS.md` byte-for-byte. When
this branch is eventually rebased onto a newer `main`, that one-line
insertion may need a trivial manual reapply if upstream also touched the
very top of the file — expected and easy to resolve, not a sign
something's wrong) and `GEMINI.md` (tracked alongside this file, same
content, for Gemini CLI).
