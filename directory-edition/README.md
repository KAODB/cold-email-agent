# cold-email-agent

A skill for one-to-one cold emails that ask an expert for advice. It finds the right person, checks every fact about them against its source page, checks the draft against seven writing rules, and sends nothing until you approve that exact email.

Most cold-email tools are built for sales volume. This one is for a few carefully chosen people, one short question each, and a report back once you've acted on their advice.

## How it works

You give a topic (what you're working on and what you need) and a direction (what kind of person to ask). The `reach-out` skill then:

1. Picks people from your candidate list, or finds the decision maker at an organization you name.
2. Verifies every fact about each person on its source page; anything it can't check stays out.
3. Screens out people who shouldn't get an email.
4. Pairs a gift: something useful to their work that you bring along.
5. Drafts by seven writing rules and checks the draft.
6. Shows you each email with a table of where every fact came from, and sends only after you say send for that version.
7. Logs it, and after a reply, helps you act on the advice and write the report-back email.

## What it runs, sends and fetches

- **Runs**: no scripts. The draft check uses standard shell tools (for example `wc -w`) on the draft file.
- **Fetches**: public web pages, to verify facts about each person and, when you name an organization, to search public profiles and recent papers.
- **Sends**: only the emails you approve one at a time, from your own signed-in webmail through a browser automation tool. LinkedIn notes are drafted only; you send them yourself.
- **Reads**: your mailbox, read-only, and only when you ask it to check for replies from people in your log.
- **Stores**: everything in a local folder, `$REACH_OUT_DIR` (default `~/reach-out/`): your candidate list, log and sent letters. The plugin has no server and collects no data.

## Setup

On first use the skill creates its files in `$REACH_OUT_DIR` and asks you to fill in `settings.md` (your signatures, how to write your title, who not to contact for now). The folder holds other people's contact details, so keep it private.

This is the directory edition. The full version on GitHub adds `check_draft.py`, a small Python script that runs the same draft checks: https://github.com/KAODB/cold-email-agent

## Limits, on purpose

- One-to-one, relevant, low-volume outreach. No bulk campaigns, no sequences, no automated follow-ups.
- Addresses come from what the person or their organization published. An address inferred from the organization's published pattern is marked "inferred" with its evidence; shared inboxes are never used.
- Rules on unsolicited email differ by country; check the recipient's before sending.

License: MIT
