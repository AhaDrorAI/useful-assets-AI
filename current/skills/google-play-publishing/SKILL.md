---
name: google-play-publishing
description: Guide a developer through publishing an Android app on the Google Play Store. Use when the user asks about Play Console, AAB, app signing, Data Safety, D-U-N-S registration, personal vs organization accounts, closed testing, the 12-tester rule, store listing, content rating, target SDK, review rejection, or any step in the Google Play submission process. Diagnoses the user's stage, builds a tailored checklist, explains the account-type choice, and walks through common rejection reasons with fixes.
metadata:
  last_reviewed: "2026-11-18"
  review_every_days: "90"
---

# Google Play Publishing

Use this skill to guide a developer — especially an independent or first-time developer — through publishing an Android app on Google Play Store.

The goal is a live, approved app, not just a submitted APK.

## Volatile facts

Google changes Play rules often. The facts below were checked on 2026-11-18. If you can browse, re-check any fact the user's next step depends on before you state it. If you cannot browse, say "as of November 2026" when you state it.

| Fact | Value as of 2026-11-18 | Source |
|---|---|---|
| Closed-testing rule | Personal accounts created after 13 November 2023 need a closed test with at least **12** testers, opted in continuously for the **14** days before applying for production access | https://support.google.com/googleplay/android-developer/answer/14151465 |
| Who the rule applies to | New personal accounts. Organization accounts are not subject to it. | same page |
| Organization accounts | Need a D-U-N-S number | https://support.google.com/googleplay/android-developer/answer/13634885 |
| Target SDK | Check the current deadline before stating it | https://developer.android.com/google/play/requirements/target-sdk |
| Registration fee | USD 25, one time | Play Console sign-up page |

Older guides say 20 testers. That number is out of date. Do not repeat it.

## Core Rules

- Diagnose the user's current stage before prescribing steps.
- Prefer targeted questions over assumptions about project state.
- If the account type is unclear, explain the personal vs organization choice (Step 2) before you plan testing.
- If the account is personal and was created after 13 November 2023, closed testing is required. Do not suggest a way around it.
- Do not recommend paying for testers or joining tester-exchange schemes. Testers must be real users who install and use the app; Google can reject or penalise fake engagement.
- Verify AAB format before store submission — APK-only is not accepted for new apps.
- Warn explicitly about Data Safety section mismatches — they are a leading rejection cause.
- Do not generate Privacy Policy text unless the user specifically asks.

## Workflow

### 1. Diagnose the current stage

Ask these in one message. Skip any the conversation already answers:

1. Do you have a Google Play Developer account? If yes: personal or organization, and roughly when was it created?
2. Is the app built and signed, or still in development?
3. Have you submitted before, or is this the first time?
4. Are you an independent developer or part of an organization?

Map the answer to one of these stages:

| Stage | Condition |
|---|---|
| Account setup | No Play Console account yet |
| D-U-N-S registration | Registered business chose an organization account, no D-U-N-S yet |
| Technical prep | Account exists, app not yet built as AAB |
| Store listing | AAB ready, listing not yet created |
| Testing | Listing complete, no testing track started |
| Submission | Testing passed or waived, not yet submitted |
| Review fix | App in review or rejected |
| Post-launch | App live, ongoing maintenance needed |

### 2. Account setup

**Cost:** $25 one-time registration fee (paid by credit card to Google).

**Account type decision:**

| Type | When to use | Verification required |
|---|---|---|
| Personal | Individual developer or hobbyist | Government-issued ID + physical Android device |
| Organization | Company, NGO, or registered business (confirm sole-proprietor eligibility) | Business documents + D-U-N-S number |

**Personal accounts created after 13 November 2023** must pass the 12-tester / 14-day closed test before production access.

**Choosing the type:** An organization account must represent a real organization. If the user has a registered business (in Israel, for example, an עוסק פטור or עוסק מורשה with its own D-U-N-S number), an organization account is a legitimate option and avoids the closed-testing rule. If the user is a private individual, use a personal account and plan for the closed test. Google's rule for sole proprietors is not clearly published: tell the user to confirm eligibility in Play Console or with Play support before they register. The account type cannot be changed from organization back to personal.

Play Console URL: https://play.google.com/console/

### 3. D-U-N-S number (organization path)

Use this step only if Step 2 chose an organization account. A D-U-N-S number identifies the business to Google. Organization accounts are not subject to the closed-testing rule.

**Process:**

1. Go to Dun & Bradstreet: https://www.dnb.com/
2. Apply for a free D-U-N-S number.
3. Processing time: from several days to about a month. Plan for a month.
4. Use the **exact same name and address** in Play Console as registered with D&B.
   - Even minor differences (abbreviations, punctuation) cause verification delays.
5. After verification, Google may contact you via email to confirm Organization status.

After verification, check whether Play Console offers a production release without a closed test. If it does not, follow Step 8.

### 4. Technical preparation

#### Build format

New apps must be submitted as **Android App Bundle (AAB)**, not APK.

Build AAB in Android Studio:

```
Build → Generate Signed Bundle / APK → Android App Bundle
```

Or via Gradle:

```bash
./gradlew bundleRelease
```

Output: `app/build/outputs/bundle/release/app-release.aab`

#### Play App Signing

Enable Play App Signing in Play Console before the first upload:

```
Release → Setup → App signing
```

Google manages the release key. You keep the upload key. If you lose the upload key, you can request a reset.

**Do not** upload directly with your local keystore as the release key for new apps — use Play App Signing.

#### API level compliance

Target SDK must meet Google's current requirement.

**Requirement noted at last review (unverified, check the link below before you state it):** from 31 August 2026, Android 16 (API level 36) or higher.
Exceptions: Wear OS and Android TV apps have separate deadlines.
Failure to comply causes the app to become invisible to new users on newer Android versions.

Check the current requirement at:
https://developer.android.com/google/play/requirements/target-sdk

In `build.gradle` or `build.gradle.kts`:

```kotlin
android {
    compileSdk = 36
    defaultConfig {
        targetSdk = 36
        minSdk = 24
    }
}
```

#### Pre-launch checks

Run these before upload:

```bash
# Check for crashes on startup
./gradlew connectedAndroidTest

# Lint warnings that block upload
./gradlew lint
```

### 5. Privacy Policy and Data Safety

Both are required before submission. They must be **consistent with each other**.

#### Privacy Policy

- Must be hosted at a publicly accessible URL (not a file attachment).
- Must describe what data is collected, how it is used, and who it is shared with.
- Free generators: PrivacyPolicies.com, Termly, or similar.
- Add the URL in Play Console under **Store listing → Privacy Policy**.

#### Data Safety Section

Location in Play Console: **Policy → App content → Data safety**

Fill every field accurately. Common rejection cause: declaring "no data collected" when the app includes a third-party SDK (Firebase, Ads, Analytics) that does collect data.

Checklist for Data Safety:

- [ ] List all data types collected (location, device ID, email, etc.)
- [ ] Specify whether data is shared with third parties
- [ ] Note whether data collection is optional or required
- [ ] Mark whether encryption is used in transit and at rest
- [ ] Review all third-party SDKs — each SDK's data practices must be included

### 6. Store listing

Required fields:

| Field | Notes |
|---|---|
| App name | Up to 30 characters |
| Short description | Up to 80 characters |
| Full description | Up to 4,000 characters — do not use only keywords |
| App icon | 512×512 px, PNG, no transparency |
| Feature graphic | 1024×500 px |
| Screenshots | At least 2 phone screenshots |
| Content rating | Complete the questionnaire — see Step 7 |
| Category | Choose the most specific relevant category |

Screenshots must accurately represent actual app screens. Using mockups that show features not in the current version is a rejection reason.

### 7. Content rating

Location: **Policy → App content → Content rating**

Complete the IARC questionnaire honestly. Inaccurate ratings cause rejection and may result in account suspension.

Common mistake: marking "no violence" for a game that includes stylized combat.

### 8. Testing tracks

Google requires staged testing before production for most new accounts.

Track order:

```
Internal Testing → Closed Testing → Open Testing → Production
```

#### Internal Testing

- Up to 100 testers.
- No review required.
- Instant distribution.
- Use for initial smoke tests.

Add testers: **Release → Internal testing → Testers**

#### Closed Testing (Alpha)

- Required for personal accounts created after 13 November 2023.
- At least 12 testers, opted in continuously for the 14 days before you apply.
- Testers must install and use the app, not only join the track.
- Recruit about 15 testers so one dropout does not put you under 12.
- After 14 days, apply for production access from the Play Console prompt. Google can still refuse; if it does, read the reason, fix it, and continue testing.

Where to find testers: friends, colleagues, a user community you belong to, or a waitlist. Do not pay for testers.

#### Open Testing (Beta)

- Optional but recommended for larger apps.
- Public opt-in, no invitation required.

### 9. Submission and review

Before submitting to production:

- [ ] All store listing fields are complete
- [ ] Data Safety section matches Privacy Policy
- [ ] Content rating questionnaire completed
- [ ] AAB uploaded and passes pre-launch report
- [ ] App does not crash on first launch
- [ ] No placeholder content ("Lorem ipsum", empty screens)
- [ ] App has actual functionality — not just a web view of an existing site
- [ ] All declared permissions are actually used
- [ ] No permissions requested that are not needed

Submit: **Release → Production → Create new release**

Review time: typically 2–7 business days for first submission. Submit well before your intended release date.

**Warning:** Repeated rejections can lead to app suspension. Fix all flagged issues before resubmission and document every change made.

#### Common rejection reasons and fixes

| Rejection reason | Fix |
|---|---|
| Thin content | Add real functionality; remove placeholder text |
| Policy violation — Deceptive behavior | Remove misleading descriptions or screenshots |
| Misleading metadata | Match screenshots to actual app content |
| Dangerous permissions | Remove unused permissions from `AndroidManifest.xml` |
| Data Safety mismatch | Update Data Safety section to include all SDK data practices |
| Crashes at launch | Fix crash before resubmission |
| Missing Privacy Policy | Add accessible URL to store listing |
| Broken Privacy Policy link | Verify URL is live and publicly accessible — a broken link is treated the same as missing |
| Content rating mismatch | Redo the IARC questionnaire accurately |
| Inconsistent developer info | Ensure name and address match exactly across Play Console, D-U-N-S, and official ID |

### 10. Post-launch maintenance

- **Monitor Vitals:** Play Console → Android Vitals — crash rate and ANR rate must stay below policy thresholds.
- **Respond to reviews:** Reply to low-rated reviews that report a bug or a misunderstanding. A fast reply is better than a late one.
- **Update target SDK:** Google enforces annual SDK updates — missing the deadline causes the app to become unavailable for new downloads.
- **Check policy emails:** Google sends warnings before enforcement — do not ignore them.
- **Stay updated:** Google Play policies and requirements change frequently. Check the Play Console Help Center and Android developer blog regularly.
- **Staged rollout:** For major updates, use staged rollout (10% → 50% → 100%) to catch regressions.

## Failure Modes

- If the user uploaded an APK instead of AAB, stop and explain the format requirement.
- If the user has a personal account and fewer than 12 testers, help them recruit real testers. Do not steer them to an organization account unless they have a real organization.
- If Data Safety was filled out quickly without checking third-party SDKs, flag this as a likely rejection cause.
- If the app was rejected without a clear reason, request appeal through Play Console support and document all changes before resubmission.
- If the user asks about removing permissions or features to pass review, verify they are truly unused before removing — do not blindly strip permissions.

## Final Checklist

At the end of any publishing session, confirm:

```text
Publishing status:

Account:
- [ ] Developer account active
- [ ] Account type: Personal / Organization
- [ ] D-U-N-S registered (if Organization)

Technical:
- [ ] AAB built and signed
- [ ] Target SDK meets current requirement
- [ ] No launch crashes

Policy:
- [ ] Privacy Policy URL live and accessible
- [ ] Data Safety section complete and accurate
- [ ] Content rating questionnaire completed

Store listing:
- [ ] App name, descriptions, icon, feature graphic complete
- [ ] Screenshots are accurate and up to date

Testing:
- [ ] Internal testing passed
- [ ] Closed testing: 12 testers / 14 days, or not required (organization account)

Submission:
- [ ] Production release created
- [ ] Review status monitored
```
