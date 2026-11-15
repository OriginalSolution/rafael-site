# Rafael: hand-off note

_Last updated 15 Nov 2026 (times are Africa/Accra, which is UTC+0). The canonical copy is in [`OriginalSolution/rafael-site`](https://github.com/OriginalSolution/rafael-site/blob/main/HANDOFF.md). Identical copies are in [`rafael-android`](https://github.com/OriginalSolution/rafael-android/blob/main/HANDOFF.md) and [`rafael-kids-browser`](https://github.com/OriginalSolution/rafael-kids-browser/blob/main/HANDOFF.md)._

This note assumes you know nothing about the project. **It contains no passwords, keys, tokens, keystores or card numbers.** It names each secret and says where it lives. All three repos are **public**.

---

## 1. What Rafael is

**Rafael** is an Android app the user turns on **voluntarily**. It blocks gambling, porn, chosen apps, websites and phone numbers for a **timed commitment** that the user picks.

- **There's no early unlock.** Once a commitment starts, it runs to the end. During a commitment the user can only make the rules *tighter* (add items, shorten allowed times).
- **Emergency calls are always reachable.** Chosen numbers (for example, family) can be marked "always reachable".
- **Honest-limits copy everywhere.** Never claim Rafael can't be bypassed, and say what it can't do. Examples: usage-based app blocking reacts after a split second, and texts from blocked numbers aren't blocked.
- **Brand:** hot orange with glossy black glassmorphism and the **wing-R** mark. The light theme is an "angelic" warm white. Chosen designs: Halo (dark), Angelic white (light), the "Shield wings" blocked screen, a Cards commitment screen, a PIN pad setup code, and a pledge with a hold-to-start button.
- Website: **https://userafael.com** (landing page, "For parents" section, FAQ, privacy page, testimonials area).

**Rafael Kids Browser** is a sister app: an Android **web browser for children**.

- **White and orange** brand, so it stands apart from the main app.
- Meant to be a **worldwide** app: copy works in any country, and all strings are ready for translation.
- **Protected from the first launch:**
  - about 937k adult domains and about 279k gambling domains (Block List Project);
  - explicit words in addresses and searches;
  - SafeSearch forced on Google, Bing and DuckDuckGo;
  - proxies, IP URLs, downloads and incognito blocked;
  - an optional Cloudflare Family DNS-over-HTTPS check.
- **Parent area behind a PIN:** the parent's own block and allow lists, an allowed-sites-only mode, category switches, history and home shortcuts.
- **Optional "Locked mode"** makes the browser the Android **device owner**:
  - installs need the PIN;
  - Bluetooth, USB file transfer, safe mode, factory reset from Settings and developer options are off;
  - the browser can't be uninstalled, and other browsers are hidden;
  - a parent can allow installs for 15 minutes or 1 hour, and can turn Locked mode off with the PIN.

### Current state (14 Nov 2026)

| Product | Latest | State |
|---|---|---|
| Rafael (Android) | **v0.5.1-poc** (versionCode 9, `app.rafael.poc`) | Public GitHub pre-release. **Works on the owner's Huawei.** On the **Samsung Galaxy Z Fold 6**, Android 13+ "restricted settings" for sideloaded apps lock Accessibility *and* Usage access. The app guides users through the one-time App info › ⋮ › *Allow restricted settings* unlock, but it's still confusing. **Plan: publish on Google Play** (store installs avoid the lock) under **Medit USA LTD** once its developer account and D-U-N-S number are ready. |
| Rafael Kids Browser | **v0.2.0-poc** (versionCode 2, `com.userafael.kidsbrowser`) | Public GitHub pre-release. **Not yet tested on a real device**; there are only unit tests (44) and Paparazzi renders, because the emulator wouldn't boot on the build box. Ask the owner whether sites now load (v0.1.0 had a "sites not opening" bug; the likely cause, a 0-px-tall WebView, is fixed in 0.2.0). |
| userafael.com | Live on GitHub Pages | HTTPS certificate approved 14 Nov 2026, expires about 12 Feb 2027, and GitHub renews it automatically. Enforce HTTPS is on. |

**Google Play will need:** permission declarations and a demo video for **Accessibility** (optional faster blocking), **Usage access**, **VpnService** (DNS website filter), call screening and, for the Kids Browser, **device owner / device admin** use. Plus a privacy policy that has had a legal review.

---

## 2. Repositories

All are owned by GitHub account **OriginalSolution**, all are **public**, and all use only the **`main`** branch. None has any GitHub Actions secrets (checked through the API on 14 Nov 2026).

| Repo | What | Deploy / release |
|---|---|---|
| [rafael-site](https://github.com/OriginalSolution/rafael-site) | Static landing page (`index.html`, `styles.css`, `main.js`, `privacy.html`, `testimonials.json`, `assets/`, `CNAME` = `userafael.com`, `.nojekyll`). | **GitHub Pages from `main` (root)**. A push to `main` deploys. The monitor lives in `.github/`. |
| [rafael-android](https://github.com/OriginalSolution/rafael-android) | Main Rafael app (Kotlin + Jetpack Compose, minSdk 26, target 35). | GitHub **pre-releases** tagged `vX.Y.Z-poc`, with asset **`Rafael-vX.Y.Z-poc.apk`**. Releases v0.1.0 to v0.5.1. |
| [rafael-kids-browser](https://github.com/OriginalSolution/rafael-kids-browser) | Kids Browser (Kotlin + Compose, minSdk 26, target 35). | Pre-releases tagged `vX.Y.Z-poc`, with asset **`Rafael-Kids-Browser-vX.Y.Z-poc.apk`**. Releases v0.1.0 and v0.2.0. |

Latest asset SHA-256 values (GitHub shows them too):
- `Rafael-v0.5.1-poc.apk`: `63f8084667f6614a082eaafc5f751d8dc0f7d518a227c5496e7e91f1ccf2919f`
- `Rafael-Kids-Browser-v0.2.0-poc.apk`: `0b8c9603bec828ea6cf402bb994fb5d867b6a75671e38d162059bf765e3172f5`

Brand source files (not in git) are on the Grok Bot box at `/workspace/rafael-brand/`, including `Rafael_Brand_Assets_v2.zip`, the design mock-ups and the PNG marks.

---

## 3. Domain and DNS

- **userafael.com** was registered at **Hostinger** on 13 Nov 2026:
  - order **65193097**;
  - **$9.99** for the first year, paid with the owner's Mastercard (card details are never stored anywhere in git);
  - **auto-renew on at $20.19/yr, next on 17 Oct 2027**;
  - WHOIS privacy on;
  - **no Hostinger hosting plan**, because the site is hosted on GitHub Pages.
- **DNS** uses Hostinger's nameservers (`aster.dns-parking.com`, `helios.dns-parking.com`), with records pointing at GitHub Pages:
  - apex `A` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`;
  - `AAAA` → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`;
  - `www` `CNAME` → `originalsolution.github.io`.
- **If HTTPS ever gets stuck** (it did once): in the rafael-site repo, Settings › Pages, remove the custom domain, add `userafael.com` again, wait for the certificate, then tick **Enforce HTTPS**. The site is down for about a minute while you do this.

---

## 4. Services and accounts (who logs in where)

| Service | Identity | Notes |
|---|---|---|
| GitHub | **OriginalSolution** | Owns all three repos. On the Grok Bot box, `gh` is logged in as `riddimbossy-prog`, which has push access. Commits are authored as `Original Solutions <296732082+OriginalSolution@users.noreply.github.com>`. |
| Hostinger (domain) | The owner's Hostinger account; its login email is **stored in the Grok Bot vault** and reachable through the Hostinger connectors on Grok Bot. | Registrar and DNS for userafael.com. The owner's other domains (nsaabo.com, kampuzz.app) are in the same account. |
| Medit Gmail | **meditusa2023@gmail.com** | Back channel: emails whose subject starts with **"Rafael fix"** are picked up and answered in the same thread. It's also the **only** destination for payment emails. The owner wants every payment-provider application made with this address. |
| Google Play Console | **Medit USA LTD** (pending approval) | Planned store for both apps. |
| Apple Developer | Medit USA LTD (pending; needs a **D-U-N-S** number) | Free lookup or request: https://developer.apple.com/enroll/duns-lookup/ |
| Cloudflare Family DNS (1.1.1.3, DoH) | No account | Used by the Kids Browser as an extra check that fails open. |

Company documents for Medit USA LTD (incorporation, forms, bank, ID) are on the Grok Bot box in `/home/box/secrets/medit-usa-ltd/`. They are private and never go in git.

---

## 5. Secrets: names and locations only

| Secret | Where it lives | Used by |
|---|---|---|
| Android release keystore `rafael-release.jks` | `/home/box/secrets/rafael-android/rafael-release.jks` on the Grok Bot box | **Both** Android apps. Certificate SHA-256 `39c534c6e36939fbe96d75125ab22c928638b2d9f434a504f7ffae8b1c60f244`. |
| `keystore.properties` (keys: `storeFile`, `storePassword`, `keyAlias`, `keyPassword`) | `/home/box/secrets/rafael-android/keystore.properties` | Gradle release signing |
| GitHub Actions secrets | **None.** The monitor uses only the built-in `GITHUB_TOKEN`. | |
| Hostinger and other logins | Grok Bot vault | |

**Back up the keystore.** If it's lost, no update can ever be installed over existing installs, and Play App Signing upload would need to be reset. Pending decision: give the Kids Browser **its own key** before Play.

**Environment variables used in builds (names only):**
- `RAFAEL_SIGNING_PROPS`: optional path to `keystore.properties`. The default is the path above. Without the file, `assembleRelease` produces an unsigned APK.
- `JAVA_HOME`: JDK 17 (the box uses `/home/box/tools/jdk-17.0.21+9`).
- `ANDROID_HOME`: Android SDK (`/home/box/tools/android-sdk`; build-tools 35.0.0).
- `source /home/box/tools/env.sh` sets both.
- Monitor (Actions only): `GITHUB_TOKEN` (built in) and `MONITOR_STATE`.

Never commit `local.properties`, `*.jks`, `keystore.properties`, `.env` files or anything from `/home/box/secrets/`.

---

## 6. Costs and renewals

- userafael.com: $9.99 paid on 13 Nov 2026; **auto-renews at $20.19 on 17 Oct 2027**.
- GitHub (public repos, Pages, Actions): $0.
- Google Play ($25 one-time) and Apple ($99/yr) under Medit USA LTD haven't been paid by this bot. Each needs the owner's yes.

---

## 7. Automation

1. **GitHub Actions monitor / Guardian** in rafael-site (upgraded in the `guardian` PR; see section 11), at [`.github/workflows/monitor.yml`](https://github.com/OriginalSolution/rafael-site/blob/main/.github/workflows/monitor.yml) with `.github/monitor/{monitor.py, monitor_lib.py, checks.json}`.
   - Runs every **6 hours** (cron `23 */6 * * *`) and can also be started by hand.
   - Checks the home page ("Take back control"), the privacy page, HTTPS, the GitHub Pages build, and that the **latest `Rafael-v*.apk`** release asset in rafael-android downloads.
   - Opens an issue labelled **`monitor`** when a check fails and closes it when the check passes again.
   - The **only auto-fix is triggering a Pages rebuild.**
   - Doesn't use any Grok credits. Edit `checks.json` to add checks, for example the Kids Browser APK.
2. **Grok Bot routine "Rafael daily self-check"**, about **9:00 AM Africa/Accra** daily.
   - Checks the site, Pages, HTTPS and the latest APK, and reads the Medit Gmail for **"Rafael fix"** emails, fixing the issue and replying in that thread.
   - **Quiet unless something needs action.** Rafael has no payments yet, so it sends no payment emails.
   - Keep any Grok routine to **once or twice a day at most**; the owner's usage is limited.

---

## 8. Open issues and pending decisions

**Site**
- The contact email **hello@userafael.com is a placeholder with no inbox.** The owner needs to choose: set up a mailbox or forwarding, or swap in another address.
- The **privacy page needs a legal review** before submitting to Play.
- The download button shows the **"-poc"** version suffix.
- Testimonials are empty. Only real ones may be added (see section 9.4).

**Rafael Android**
- Samsung restricted-settings friction is the reason for going to Play. Waiting on the owner's Z Fold 6 feedback.
- The PIN doesn't lock a child out of changes in the main app; it only protects the commitment. Don't market it as a parental lock.
- Play listing and declarations are to be prepared once the Medit USA accounts are approved. The D-U-N-S request is still to do (the bot offered to help).

**Kids Browser (decisions for the owner)**
1. White labels on orange buttons look on-brand, but the contrast is only about 3.3:1. Black labels would be easier to read.
2. Dark mode is off by default and follows the phone only when the parent turns that on. Keep this?
3. Locked mode also turns off **developer options/adb** and **app management**. That's safer, but you can't debug a locked device.
4. Use a **separate signing key** before Play?
5. Locked-mode QR setup (`docs/locked-mode/` in that repo) downloads the v0.2.0 APK from the public release URL.
6. If the PIN is forgotten while Locked mode is on, the only way out is a factory reset from the recovery menu.

**Next features (research, 14 Nov 2026), top five:**
1. School hours, bedtime and Homework mode.
2. A weekly report a parent can share (on the device, no account).
3. Data Lite (list updates on Wi-Fi only, ad and tracker blocking, text-first mode).
4. Profiles for children sharing one device.
5. Warnings for risky links, scams and grooming words, checked only in the browser, and never reading chats.

After those, worldwide translations and regional school shortcut packs.

---

## 9. Standing rules from the owner (Riddim Boss)

- **Every charge** on the owner's card needs his **yes in chat** first. Report spending to his "Chief of Staff" bot.
- **Never send messages or emails unasked.** The only standing exceptions are payment reports and "Rafael fix" thread replies to **meditusa2023@gmail.com**.
- **Publishing releases, going live with payments, spending money and destructive changes** need his yes in chat.
- **Keep secrets out of git** (all repos are public).
- **Never invent testimonials or data.**
- **Work lean:** his usage limits are tight. Prefer the free GitHub Actions monitor over Grok routines.
- He likes visual or animated design options (videos) and picks by replying to them.

---

## 10. How to build, test, sign and release

### 10.1 Android (same for both apps; run in the repo root)
```bash
source /home/box/tools/env.sh            # or export JAVA_HOME (JDK 17) and ANDROID_HOME
./gradlew testDebugUnitTest              # unit tests (Kids Browser: 44)
./gradlew assembleRelease                # signed when keystore.properties is found
APK=app/build/outputs/apk/release/app-release.apk
$ANDROID_HOME/build-tools/35.0.0/apksigner verify --print-certs "$APK" | grep SHA-256
#   must print 39c534c6e36939fbe96d75125ab22c928638b2d9f434a504f7ffae8b1c60f244
$ANDROID_HOME/build-tools/35.0.0/aapt2 dump badging "$APK" | head -1   # check versionCode/versionName
```
Toolchain: JDK 17, Gradle 8.11.1 (wrapper), AGP 8.7.3, Kotlin 2.0.21. Before each release, bump **`versionCode`** (+1) and **`versionName`** (`X.Y.Z-poc`) in `app/build.gradle.kts`.

### 10.2 Release (needs the owner's yes before publishing)
```bash
cp "$APK" /workspace/out/Rafael-vX.Y.Z-poc.apk            # Kids: Rafael-Kids-Browser-vX.Y.Z-poc.apk
sha256sum /workspace/out/Rafael-vX.Y.Z-poc.apk
git -c user.name="Original Solutions" -c user.email="296732082+OriginalSolution@users.noreply.github.com" commit -am "vX.Y.Z-poc: …"
git tag vX.Y.Z-poc && git push origin main vX.Y.Z-poc
gh release create vX.Y.Z-poc /workspace/out/Rafael-vX.Y.Z-poc.apk -R OriginalSolution/<repo> \
  --draft --prerelease --title "… vX.Y.Z-poc" --notes-file notes.md   # put the SHA-256 in the notes
# after the owner says yes:
gh release edit vX.Y.Z-poc -R OriginalSolution/<repo> --draft=false
```
After publishing, download the asset and check that its SHA-256 matches. Every build is signed with the same key, so updates install over older versions. Sideload help for Samsung: turn off **Auto Blocker** (Settings › Security and privacy › Auto Blocker) and tap **Install anyway** if Play Protect asks.

UI renders: both apps were rendered with Paparazzi 1.3.5, which is added to Gradle only temporarily. The Kids Browser render source is in `docs/render/*.kt.txt`, and the outputs are in `docs/smoke/`.

### 10.3 Website deploy
Edit the files in rafael-site and push to `main`. GitHub Pages publishes within about a minute. Keep `CNAME` (`userafael.com`) and `.nojekyll`. Check https://userafael.com afterwards, or run the monitor workflow by hand (Actions › monitor › Run workflow).

### 10.4 Testimonials
Add **only real stories, shared with the person's permission,** to `testimonials.json` in rafael-site. Each entry is an object with `quote` (required), and optionally `name`, `detail` and `"anonymous": true`. While the list is empty, the site shows a "Be one of the first stories" card. Full steps are in `TESTIMONIALS.md`.

### 10.5 Kids Browser block lists
`python3 tools/build_blocklists.py` rebuilds `adult.bin` and `gambling.bin` (FNV-1a 64-bit hashes) from the Block List Project lists (The Unlicense). See that repo's README.

---

## 11. Guardian (watchdog), added 15 Nov 2026 in the `guardian` PRs (waiting for the owner's yes to merge)

It's modelled on Betspapa's Papa Guardian (Betspapa PR #72), which reports a status of `ok` or `attention` with a plain reason and repairs what it can. It uses only the built-in `GITHUB_TOKEN`: no secrets, no spending, no email.

### rafael-site: `.github/workflows/monitor.yml` and `.github/monitor/guardian.py`
- **When it runs:**
  - every 6 hours (cron `23 */6 * * *`);
  - on **`page_build`**, which is the "boot" check after every GitHub Pages deploy;
  - by hand (Actions › Guardian › Run workflow);
  - on pull requests, as unit tests plus a **dry run** (no issues, repairs, dispatch or state).
- **What it checks**, each with **exponential backoff** (4 tries, waiting 2, 4 then 8 s):
  - the home page (text "Take back control") and the privacy page;
  - HTTPS (the certificate must have 10 or more days left);
  - the GitHub Pages build;
  - the latest `Rafael-v*.apk` and `Rafael-Kids-Browser-v*.apk` release downloads (a 1-byte ranged GET).
- **Auto-repair:**
  - re-requests a Pages build when the last build errored;
  - keeps the **last good data**: if a newest APK fails, it checks that the last good APK still downloads and puts that in the reason;
  - a hung run is killed after 6 minutes, and runs never overlap (concurrency group `guardian`).
  - It never edits main or the live site and never deletes anything.
- **Health check:**
  - `health.json` on the **`guardian-state`** branch: https://raw.githubusercontent.com/OriginalSolution/rafael-site/guardian-state/health.json
  - Format: `{service, status: "ok"|"attention", reason, checked_at, consecutive_attention, last_ok_at, checks[], run}`.
  - It isn't served from userafael.com, on purpose: writing to main on every run would rebuild the site 4+ times a day.
- **Incident log:** `incidents.jsonl` on `guardian-state`. It's append-only, one JSON line per event, with `kind` = `opened`, `resolved`, `repair` or `dispatch`.
  - Also on that branch: `last_good.json` (the last all-passing run and the last good APK URLs) and `state.json` (counters).
  - One **`monitor` issue** per failing check is opened, updated, and closed automatically when the check passes again.
- **Escalation:** when `attention` lasts **2 runs in a row** (about 12 hours), it sends `repository_dispatch` with event type **`guardian-attention`** to this repo, then again every 4 runs while the problem continues.
  - The payload is `{source, status, reason, consecutive_runs, run_url}`.
  - `.github/workflows/guardian-attention.yml` receives it and records it in a `guardian`-labelled issue.
  - The owner's planned AI fixer can listen for the same event.
  - repository_dispatch only triggers workflows that are on the default branch, so the receiver works **after merge**.
- **Tuning:** the `guardian` block in `.github/monitor/checks.json` sets `attention_after_runs` and `redispatch_every_runs`.
- **Tests:** `cd .github/monitor && python3 -m unittest -v guardian_test`.

### rafael-android and rafael-kids-browser: `.github/workflows/ci.yml`
- Runs on every push and pull request to `main`, and by hand:
  - JDK 17 (Temurin) and the Android SDK (platform 35, build-tools 35.0.0);
  - `./gradlew testDebugUnitTest` then `./gradlew assembleDebug`;
  - test reports are kept as an artifact for 7 days.
- **No signing, keystore or release step**, so CI can never publish an APK. Releases stay manual and need the owner's yes (section 10).
- **Guardian job:** when CI fails on a push to `main` and the previous `main` run also failed, it sends `repository_dispatch` `guardian-attention` (`source: ci`) to that repo.
- **No health endpoint:** these are on-device apps with no server, so there's nothing to probe. Their public health is covered by the rafael-site Guardian's APK download checks.
