# Earlier thread (transcript)

**User:** Ship platesnap 2.4.0 to TestFlight, then submit for App Store review once the build processes.

**Assistant:** Bumped `MARKETING_VERSION` to 2.4.0 and build number to 312 in `project.yml`, regenerated the project, committed `chore(release): 2.4.0 (312)` and pushed to `main`. Archive and upload succeeded; build 312 is processing in App Store Connect.

**User:** ok ping me when it's ready, I'll write the release notes meanwhile

**Assistant:** Will do. Build 312 finished processing and is available in TestFlight for internal testers. I have not submitted for review yet — I need the release notes from you first.

**User:** [pastes Swedish and English release notes]

**Assistant:** Set the English notes. The Swedish locale rejected the text: "Promotional text exceeds 170 characters" — I had put the notes in the wrong field. Retrying in What's New.

[thread ends here]

# Live state (what tools return right now)

`git status` on `main`: clean, up to date with origin. `git log -1 --oneline`: `9be2d10 chore(release): 2.4.0 (312)`

App Store Connect: the `asc` CLI is not authenticated in this session (`asc: not logged in`); App Store Connect state cannot be read.
