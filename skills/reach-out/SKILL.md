---
name: reach-out
description: "Cold mail agent. The user gives a topic plus a reach-out direction, and a fixed workflow produces a cold email ready to send: pick recipients (candidate list, or the decision maker at a named organization) → verify against the original source pages → pair a gift → draft by the seven writing rules → run check_draft.py → get the user's confirmation in the conversation → send from the user's signed-in browser mailbox only after the user says send → log it → after a reply, act on the advice and report back. Triggers: cold mail, cold email, cold outreach, reach out, outreach email, email someone I don't know, write to someone, ask someone for advice, ask an expert, find a mentor, who should I contact, find the decision maker, report-back email, check for replies. Not for: high-volume B2B sales sequences (a copywriting skill can supply the copy; verification, confirmation, sending and logging still follow this workflow); application forms; public LinkedIn/X posts (use a social-post skill)."
---

# reach-out: cold mail agent

The user provides only two things: a **topic** (what they're working on and what they want) and a **direction** (what kind of person they want to reach). This workflow does everything else and stops at "waiting for the user to say send."

## Folder

All data lives in `$REACH_OUT_DIR` (if it's unset, use `~/reach-out/`). This folder holds recipients' contact details and correspondence; never put it in a public repo or a publicly shared cloud folder.

| File | Contents |
|---|---|
| `settings.md` | Personal signatures (one per language you write in), the fixed wording of the user's title, a signature for each company identity, the picking order when no direction is given, the do-not-contact-for-now list, the approved wording for unannounced projects |
| `candidates.md` | Candidates, one per row; if there's more than one list, `settings.md` sets the order to check them in |
| `gifts.md` | Things you can bring |
| `log.md` | One row per email sent |
| `letters/` | One file per sent email, with its final text |

On first use, when the folder doesn't exist yet: create the five items above, fill in the table headers, and ask the user to complete `settings.md`. Ask about any field left empty when you reach the step that needs it, and write the answer back to `settings.md`. Headers for the three tables:

```
candidates.md
| # | Name | Current role (organization) | Why a good fit | Signs they reply | Public contact channel | One specific question to ask | Source URL |

gifts.md
| Gift | Link or location | Fits which kind of person | Usable? |

log.md
| Sent on | Candidate # | Recipient | Channel | Identity | What I brought | What I asked | Status | Their advice | What I did, result | Reported back on | Letter file |
```

## The seven writing rules

| # | Rule | Why |
|---|---|---|
| 1 | Get to the point: the first sentence asks for "one piece of quick expert advice," optionally with half a sentence on why you're asking them (their research). Name and title go in the signature, not the body | The recipient knows from the first sentence what you want from them; the signature already says who you are. This replaces the common advice to open with a hook |
| 2 | Bring something first: a new piece of information, an introduction, or a result directly relevant to their work, with a link | Give before you ask: if reading leaves them with something, they have a reason to reply |
| 3 | Ask one question only: specific advice they can give in a sentence or two. No call requests; never write "could I have a few minutes of your time" | A one- or two-sentence reply costs them the least; a call asks them to set aside time |
| 4 | Keep it short: body at most 130 words in English, 250 characters in Chinese | Read in one pass, answered on the spot |
| 5 | In one sentence, say what you'll do with the advice and that you'll report back | Their advice won't be wasted, and it sets up the later report-back email (workflow step 11) |
| 6 | Don't ask for a reply at the end: no "let me know," "not sure if you saw this," or "looking forward to hearing from you"; stop when you're done | Asking for a reply applies pressure; it doesn't give a reason |
| 7 | Delete test: read the first sentence as the recipient; if you'd want to delete it, rewrite it | One last check through the recipient's eyes |

Body skeleton (follow the structure, not the wording): something about them, with a little personality → one sentence on what I did and a concrete result → it costs them little effort → one question. The first sentence still follows rule 1: the half-sentence on why you're asking them is the skeleton's "something about them."

## Workflow

1. **Read the input.** Topic and direction; anything unstated takes the defaults: 3 people, identity = personal, language = the recipient's. Ask only if the topic or direction itself is unclear, and ask everything at once.
2. **Pick people.** If the user names an organization but not a person, first follow [decision-makers.md](decision-makers.md) and get the candidate table approved. If the user didn't specify a direction, follow the picking order in `settings.md` (if none is written yet, ask once and write it back). First look in `candidates.md` for people who fit the direction (check the "Why a good fit" and "Public contact channel" columns); with more than one list, check them in the order set in `settings.md`. Never email anyone already in `log.md` again. Search the web for new people only if the list falls short; each person needs a source URL, and anyone you find goes into the list. Don't write to anyone without a public channel of their own or their organization's.
3. **Verify against the original pages.** Lists are often compiled by an agent, and descriptions have turned up that the source page never said. Every fact about the person that the email will use (current role, past work, email address) must be checked at this step by opening the source page yourself; anything that doesn't match stays out of the email. Write names exactly as the source does; never reconstruct a Chinese name from its romanization.
4. **Screen out who shouldn't get an email.** See "Who not to contact, and red lines" below.
5. **Pair a gift.** Pick one item from `gifts.md` that fits this person's work; confirm on the spot that any public link opens. If nothing fits, tell the user "this one needs something made first" and propose the smallest gift that can be done within a day; "something I'll do later" doesn't count as a gift.
6. **Draft.** Follow the seven rules above. Subject line of 8 English words or fewer, about them or the gift; never "Introduction" or "Quick question." Plain text, links as full URLs. The question should be one you can act on within 2–4 weeks and report back on. For the signature, see "Signature" below. Draft format (check_draft.py reads this):

   ```
   To: recipient email
   Subject: subject line

   Salutation,
   Body…
   --
   Signature line 1 (name)
   Signature line 2 (title)
   ```

7. **Machine check.** Save the draft to a scratch location and run `python3 "${CLAUDE_SKILL_DIR}/check_draft.py" <draft-file>` (`${CLAUDE_SKILL_DIR}` is the folder containing this SKILL.md; if it isn't substituted, replace it with the base directory shown when this skill loads). Fix every FAIL until it passes; use your judgment on WARNs.
8. **Get the user's confirmation.** For each email, give in the conversation: recipient and channel, the draft, a translation into the user's language (if the email is already in the user's language, the draft only), and a table of where each fact in the email comes from. The user can reply "send 1," "send 1, 3," or "edit 2: …".
9. **Send.** Send only after the user explicitly says send for that version of that email; if even one word changes afterward, confirm again. How: see "Sending." Keep confirming one email at a time until at least about 20 have been sent; whether to switch to batch approval is for the user to bring up; don't suggest it.
10. **Log.** After sending: save the final text to `letters/YYYY-MM-DD-surname.md` (recipient, channel, time sent, the text, its translation, source table); add a row to `log.md`; leave the person's row in the candidate list as is.
11. **After a reply.** The user says the person replied, or asks you to check for replies (search the user's mailbox for recipients in the log; read only). Record the advice in the log → agree with the user on one thing that can be done within 2–4 weeks → once it's done, draft a report-back email ("I did what you suggested; here's what happened" + the next question), again going through steps 7–10.
12. **No reply.** Don't chase. Write a second email only when you have something new that's useful to them: at most one, at least two weeks after the first, framed as "this might be useful to you," and then stop.

## Who not to contact, and red lines

- People who may be reviewing the user's manuscript (journal editors, reviewers): don't email them until the review is over. Keep them under "Do not contact for now" in `settings.md`; whenever the user submits a new manuscript, go over that list again.
- Results of papers under review stay out of emails; they can become gifts only after acceptance.
- Projects not yet public or with patents not yet granted: an email may say no more than the passage the user set under "Unannounced project wording" in `settings.md`. That wording usually covers: one sentence on what you're working on and where you're starting; why you need outside advice (e.g., confidentiality constraints, no access to a certain kind of person); what you want to ask; and that you'll act on the advice and report the results back. No organizations, specs, company names, or websites; use the personal signature. If no wording has been set, leave the project out of the email and ask the user first.
- No patient information, pending applications, or review content.
- Never write any payment or financial commitment on the user's behalf.
- Use the user's title exactly as fixed in `settings.md`; don't upgrade or reword it. Check it before writing.
- One email uses one identity's facts: personal and each company's are never mixed. When writing as a company, take the company facts and signature from the facts file you keep for that company, not from memory; before writing "we," confirm which company that means.
- Write to the person responsible for the matter, never to an organization's shared inbox. Use an address the person or their organization published. If there is none, infer the format from personal addresses the same organization published, mark it "inferred" with its basis in the confirmation table, and fix it if the email bounces; the name and the format sample each need a source page. Never take addresses from places they weren't published for contact.

## Signature

Personal (default), filled in from `settings.md`:

```
<Name in English>, <degree (omit if none)>
<Title in English, in its fixed wording>
<City>, <Country>
```

Chinese emails: `<name in Chinese> / <title> / <city>`. Show a company-identity signature to the user before its first use; once it's settled, write it into `settings.md`. check_draft.py requires the signature after the `--` line, at least two lines long.

## Sending

Use the channel recorded in the person's row of the candidate list.

- **Email**: with a browser automation tool (e.g., Claude in Chrome), open the webmail the user is signed in to (e.g., Gmail) → Compose → type the recipient, subject, and body into their fields one by one (never put content in URL parameters) → read the three fields back from the compose window and compare them word for word with the version the user confirmed; fix any difference, and stop if you can't → click Send → wait for the "Message sent" notice, then confirm the email is in the Sent folder → close the tab.
- **LinkedIn invitation note**: draft only; the user pastes and sends it (LinkedIn's User Agreement prohibits using automation tools to add connections or send messages). The length limit is whatever the screen shows (commonly 200 or 300 characters, depending on account type); also write a short version for the user to confirm.
- **Website contact form**: after filling it in, read it back and compare; submit once confirmed. If a CAPTCHA appears, stop and ask the user to get past it themselves.
- One confirmation covers one email to one recipient. No batch sending, attachments, or CCs unless the user says so explicitly that time.
- If sending fails or the status is unclear: don't click Send again; check the Sent folder first and report exactly what you find.

## Report format

The first line says which step you've stopped at and what you're waiting for the user to do. One subsection per email. Report unverified facts and unsent emails as they are; don't present them as done.
