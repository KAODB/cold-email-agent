# cold-email-agent

A Claude Code skill for one-to-one cold emails that ask an expert for advice. It finds the right person, checks every fact about them against its source page, runs a machine check on the draft, and sends nothing until you approve that exact email.

Most cold-email tools are built for sales volume. This one is for the opposite case: a few carefully chosen people, one short question each, and a report back once you've acted on their advice.

## How it works

You give two things: a **topic** (what you're working on and what you need) and a **direction** (what kind of person you want to ask). The `reach-out` skill does the rest and stops at "waiting for you to say send":

1. **Pick people** from your candidate list.
2. **Verify against the original pages.** Every fact about the person that goes into the email (current role, past work, address) is checked on its source page. Anything that can't be checked stays out.
3. **Screen out** people who shouldn't get an email, such as possible reviewers of your manuscript.
4. **Pair a gift**: something you bring that's useful to their work, such as new information, an introduction or a result.
5. **Draft** by seven writing rules, then run [`check_draft.py`](skills/reach-out/check_draft.py) until it passes.
6. **Show you each email** with a table of where every fact came from. It sends only after you say send for that version; if one word changes, it asks again.
7. **Log it**, and after a reply, help you act on the advice and write the report-back email.

## The seven writing rules

1. **Get to the point.** The first sentence asks for one piece of quick expert advice, optionally with half a sentence on why them.
2. **Bring something first**: new information, an introduction, or a result relevant to their work.
3. **Ask one question** they can answer in a sentence or two. No call requests.
4. **Keep it short**: at most 130 words in English, 250 characters in Chinese.
5. **Say what you'll do with the advice** and that you'll report back.
6. **Don't ask for a reply** at the end. Stop when you're done.
7. **Delete test**: read the first sentence as the recipient; if you'd delete it, rewrite it.

`check_draft.py` enforces the mechanical parts (length, exactly one question, banned openers and filler phrases, signature) for English and Chinese drafts.

## Install

In Claude Code:

```
/plugin marketplace add KAODB/cold-email-agent
/plugin install cold-email-agent@cold-email-agent
```

Or copy `skills/reach-out/` into `~/.claude/skills/`. The skill is a plain `SKILL.md` folder, so other agents that read skills can use it too.

## Setup

Everything the skill keeps lives in one private folder: `$REACH_OUT_DIR` (defaults to `~/reach-out/`).

| File | Contents |
|---|---|
| `settings.md` | Your signatures, how to write your title, who not to contact for now |
| `candidates.md` | People you might write to, with source links |
| `gifts.md` | Things you can bring |
| `log.md` | One row per email sent |
| `letters/` | The final text of each sent email |

On first use the skill creates these files and asks you to fill in `settings.md`. They hold other people's contact details, so keep the folder out of any public repo or shared drive.

Requirements: Python 3 for `check_draft.py` (standard library only). Emails are sent from your own signed-in webmail through a browser automation tool (for example Claude in Chrome); without one, send the approved draft yourself.

## Limits, on purpose

- One-to-one, relevant, low-volume outreach. No bulk campaigns, no sequences, no automated follow-ups.
- Nothing is sent without your approval of that exact email. LinkedIn notes are drafted only; you send them yourself.
- Addresses come from what the person or their organization published. An address inferred from the organization's published pattern is marked "inferred" with its evidence; shared inboxes are never used.
- People who decline or ask not to be contacted go on the do-not-contact list.
- Rules on unsolicited email differ by country; check the recipient's before sending.

## Self-test

```
python3 skills/reach-out/check_draft.py --selftest
```

## License

MIT
