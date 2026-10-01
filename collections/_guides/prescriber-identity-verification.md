---
title: "Verifying Prescriber Identity with ID.me"
guide_for:
- /sdk/layout-effect/
---

Surescripts requires a verified identity, also called identity proofing, before a prescriber can enroll to send electronic prescriptions. Prescribers complete this verification on their own through ID.me, without scheduling a video appointment. This guide covers how a prescriber verifies, what Canvas records when they finish, and what an EPCS Administrator follows up on afterward.

Identity verification is turned on per instance. When it is off, the provider menu has no **Identity verification** item. To turn it on, [ask Canvas Support](https://portal.usepylon.com/canvas-medical/forms/standard).

* * *

## What you'll learn

1. How to prepare a prescriber's staff profile so the verification matches it
2. How a prescriber verifies their identity with ID.me
3. What Canvas saves to the staff profile, and what it leaves for you to update
4. How an EPCS Administrator tracks which prescribers are verified
5. What each failure message means

* * *

## Prepare the staff profile

ID.me does not know which Canvas prescriber is verifying. When the prescriber starts, Canvas sends the NPI, last name, and date of birth from their staff profile. When the prescriber returns, Canvas checks the ID.me result against those values:

- **When both the staff profile and ID.me have an NPI,** the NPI decides the match. If the NPI matches, the verification succeeds even when the last name or date of birth differs. Canvas shows the difference so the practice can update the staff profile. Last names change with marriage and other legal name changes, so a name difference alone does not reject a real prescriber.
- **When there is no NPI to compare,** the last name has to match.
- **When there is nothing to compare,** the verification is rejected.

Before a prescriber verifies, check that their staff profile has the correct NPI, last name, and date of birth.

## Verify a prescriber's identity

The prescriber completes these steps themselves, logged in to Canvas with their own account. Most people finish in about five minutes. Prescribers who already have a verified ID.me account only sign in and give permission to share their details.

To verify, the prescriber needs:

- A photo of their driver's license, state ID, or passport
- A phone

1. In the provider menu, select **Identity verification**. The verification page opens in a new tab.
2. Select **Verify with ID.me**.
3. On the ID.me site, sign in or create an account, then follow the prompts to verify.
4. When ID.me returns to Canvas, confirm that the page shows **You're verified**, then select **Done**.

The verification page then shows **Your identity is verified** with the verification date and the NPI that ID.me verified. It also lists any DEA registrations ID.me returned, by state, with their expiration dates. To repeat the verification later, select **Verify again**.

## Review what Canvas saves

Canvas saves each completed verification to the prescriber's staff profile. The record includes the date, the assurance level ID.me verified to, and the details ID.me returned. Earlier verifications are kept when a prescriber verifies again. Canvas does not store the prescriber's Social Security number.

After a verification, review the staff profile for these cases:

| Case | What Canvas does | What to do |
| --- | --- | --- |
| The staff profile has no NPI | Fills in the NPI that ID.me verified. | Nothing. |
| The staff profile has a different NPI | Leaves the staff profile unchanged and shows **The NPI on this staff record does not match**. | Determine which NPI is correct and update the staff profile before enrolling the prescriber with Surescripts. |
| The NPI matches but the last name or date of birth differs | Keeps the verification and shows a warning describing the difference. | Update the staff profile if it is out of date. |
| ID.me returned DEA registrations | Shows the registrations but does not add them to the staff profile. | Add each one to the staff profile as a DEA license. ID.me does not return an issuance date, so enter it from the registration certificate. |

## Track verification across prescribers

Staff with the **EPCS Administrator** role see a **Prescribers** table below their own status on the verification page. The table lists every active staff member with their NPI, whether they are verified, and the date of their latest verification. When ID.me verified a different NPI from the one on the staff profile, the table shows the verified NPI under the staff profile NPI.

## Troubleshoot a verification that did not finish

When a verification fails, the page shows **Verification did not finish** with one of these messages. Select **Try again** to return to the verification page.

| Message | Meaning |
| --- | --- |
| Verification was cancelled before it finished. | The prescriber left the ID.me flow before completing it. |
| That verification link has already been used or has expired. | The return link from ID.me can be used only once. Start a new verification. |
| The identity ID.me verified does not match this staff record. Nothing has been changed. Check the NPI, last name, and date of birth on the record, and contact support if they are correct. | The ID.me result did not match the staff profile. See [Prepare the staff profile](#prepare-the-staff-profile). |
| ID.me could not be reached. Try again in a few minutes. | Canvas could not connect to ID.me. |
| ID.me did not complete the verification. | ID.me returned without a result. |
| ID.me verified your identity, but Canvas could not record it. Contact support before trying again. | ID.me confirmed the identity, but Canvas could not save it. [Contact Canvas Support](https://portal.usepylon.com/canvas-medical/forms/standard). |
| The verification did not complete. | Canvas could not confirm the verification, for example because the link belongs to another staff member. |
