# Your first open-source PR + hiring plan (about 1 week)

## Day 1: Pick a target
- github.com/roboflow/supervision, inference, notebooks, trackers, rf-detr
- Filter issues by `good first issue` or `help wanted`. Comment "I'd like to take this" and wait for a reply.
- No suitable issue? Docs fixes, typos, broken links, missing docstrings/type hints and extra tests are all welcome first PRs.

## Day 2-3: Contribute
1. Fork, clone, create a branch: `git checkout -b fix/short-description`
2. Read CONTRIBUTING.md; install dev deps and pre-commit hooks.
3. Make a small change with a test. Run the linter and tests.
4. Open a PR: what changed, why, how you tested it, `Fixes #123`.
5. Respond to review feedback quickly.

## Day 3-4: Ship this project
- Push `dwell-vision` to your GitHub with a demo GIF in the README.
- Possible upgrades: a FastAPI endpoint + React dashboard for dwell-time stats (shows full-stack skills), or a Dockerfile.

## Day 5: Write about it
Blog post (Dev.to / Medium): "Measuring dwell time with Roboflow supervision". Cover the problem, the approach (ByteTrack + PolygonZone), a result GIF and what you learned from your PR.

## Day 6: Follow up
Reply to the recruiter email with links to your repo, PR and post (3 lines max):
"Hi, following my application for Full Stack Engineer: I built X with supervision (link), contributed to Y (PR link) and wrote Z (link). Happy to chat."
