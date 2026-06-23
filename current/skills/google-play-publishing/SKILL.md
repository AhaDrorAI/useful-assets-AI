---
name: google-play-publishing
description: Guide a developer through publishing an app on Google Play Store. Use when the user asks about Play Console, AAB, app signing, Data Safety, DUNS registration, closed testing, tester requirements, store listing, content rating, review rejection, or any step in the Google Play submission process. The skill diagnoses which stage the user is at, generates a tailored checklist, explains the DUNS workaround for independent developers, and walks through common rejection reasons with fixes.
---

# Google Play Publishing

Use this skill to guide a developer — especially an independent or first-time developer — through publishing an Android app on Google Play Store.

The goal is a live, approved app, not just a submitted APK.

## Core Rules

- Diagnose the user's current stage before prescribing steps.
- Prefer targeted questions over assumptions about project state.
- Explain the DUNS path for independent developers whenever account type is unclear.
- Never suggest skipping the Closed Testing track without confirming DUNS Organization status first.
- Verify AAB format before store submission — APK-only is not accepted for new apps.
- Warn explicitly about Data Safety section mismatches — they are a leading rejection cause.
- Do not generate Privacy Policy text unless the user specifically asks.

## Workflow

### 1. Diagnose the current stage

Ask only what is needed to determine stage:

1. Do you have a Google Play Developer account?
2. Is the app built and signed, or still in development?
3. Have you submitted before, or is this the first time?
4. Are you an independent developer or part of an organization?

Map the answer to one of these stages:

| Stage | Condition |
|---|---|
| Account setup | No Play Console account yet |
| DUNS registration | Independent developer, no organization account |
| Technical prep | Account exists, app not yet built as AAB |
| Store listing | AAB ready, listing not yet created |
| Testing | Listing complete, no testing track started |
| Submission | Testing passed or waived, not yet submitted |
| Review fix | App in review or rejected |
| Post-launch | App live, ongoing maintenance needed |

### 2. Account setup

**Cost:** $25 one-time registration fee (paid by credit card to Google).

**Account type decision:**

| Type | When to use |
|---|---|
| Personal | Sole developer, no team, no DUNS |
| Organization | Company, NGO, or independent developer with DUNS number |

**Recommendation for independent developers:** Register as Organization using a DUNS number. See Step 3.

Play Console URL: https://play.google.com/console/

### 3. DUNS number for independent developers (Organization path)

A DUNS number lets a sole developer (including a self-employed / עוסק פטור in Israel) register as an Organization. This often waives the 20-tester / 14-day Closed Testing requirement.

**Process:**

1. Go to Dun & Bradstreet: https://www.dnb.com/
2. Apply for a free D-U-N-S number.
3. Processing time: approximately one week.
4. Use the **exact same name and address** in Play Console as registered with D&B.
   - Even minor differences (abbreviations, punctuation) cause verification delays.
5. After verification, Google may contact you via email to confirm Organization status.

**Tester requirement bypass:**
Once registered as Organization, Google may approve the app without requiring 20 testers for 14 days. This is not guaranteed — confirm after registration.

Tester community fallback (if 20 testers are required): https://www.testerscommunity.com/

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

Target SDK must meet Google's current requirement (typically `targetSdk = current year's minimum`).

Check the current requirement at:
https://developer.android.com/google/play/requirements/target-sdk

In `build.gradle` or `build.gradle.kts`:

```kotlin
android {
    compileSdk = 35
    defaultConfig {
        targetSdk = 35
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
| Feature graphic | 1024×500 px (required since 2021) |
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

- Required for new accounts without Organization status.
- Minimum 20 opt-in testers for 14 consecutive days.
- Testers must actively install and use the app (not just join the track).
- After 14 days, request production access via the Play Console prompt.

If DUNS Organization status is confirmed, this requirement may be waived — check Play Console for the production release option.

Finding testers: https://www.testerscommunity.com/

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

Review time: typically 2–7 business days for first submission.

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
| Content rating mismatch | Redo the IARC questionnaire accurately |

### 10. Post-launch maintenance

- **Monitor Vitals:** Play Console → Android Vitals — crash rate and ANR rate must stay below policy thresholds.
- **Respond to reviews:** Reply to 1-star reviews within 48 hours when possible.
- **Update target SDK:** Google enforces annual SDK updates — missing the deadline causes the app to become unavailable for new downloads.
- **Check policy emails:** Google sends warnings before enforcement — do not ignore them.
- **Staged rollout:** For major updates, use staged rollout (10% → 50% → 100%) to catch regressions.

## Failure Modes

- If the user uploaded an APK instead of AAB, stop and explain the format requirement.
- If the user has fewer than 20 testers and no DUNS, walk them through the DUNS path before tester recruitment.
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
- [ ] DUNS registered (if Organization)

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
- [ ] Closed testing: 20 testers / 14 days OR Organization waiver confirmed

Submission:
- [ ] Production release created
- [ ] Review status monitored
```
