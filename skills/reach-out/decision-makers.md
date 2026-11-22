# Finding the right decision maker

Run this before drafting whenever the user names an organization but not a person. Input: the target organization and the purpose of the outreach. Output: a short candidate table the user approves before any drafting starts.

Writing to the wrong level is the most common reason a cold email gets no reply. The goal is one or two people whose job makes the message relevant to them, not a long list.

## 1. Pick titles by organization size

A starting heuristic, not a rule:

| Organization | Titles to target | Why |
|---|---|---|
| Startup or small team (under 50 people) | Founder, CEO, CTO, co-founder | Short decision chain; founders read their own email and care about using resources well |
| Mid-size company (50–500) | VP, Head of [relevant function], Director | Holds budget and execution authority; feels the specific problem most |
| Large company or institution (500+) | Director, Senior Manager, Program Lead | C-level inboxes are filtered; middle managers are the ones who move projects |
| Academic, medical or R&D unit | PI (principal investigator), lab director, corresponding author | Start from the corresponding authors of their recent papers |

## 2. Find candidates

Use a search engine's `site:` operator on public profile pages instead of scraping:

```text
site:linkedin.com/in/ "<organization>" ("Head of" OR "VP" OR "Director") "<field>"
```

- Narrow it with a place (`"Taiwan"`, `"Boston"`) or exclusions (`-intern -recruiter`).
- For academic targets, search the field plus the institution in PubMed, Google Scholar or arXiv and read the author lists from the last two or three years.
- Search by hand or through an ordinary search engine. Don't automate logins or scraping on LinkedIn or similar sites; their terms forbid it.

## 3. Find a contact address, in this order

1. An address the person or the organization published for contact: a staff or team page, a press-release contact, a conference speaker page, the corresponding-author address on a paper.
2. An inferred address (for example `firstname.lastname@domain`), only when personal addresses the same organization published confirm the pattern. Mark it "inferred" in the table with its basis (the sample address and its source page), so the user sees it before approving the send. If it bounces, fix it from the evidence instead of guessing again.

Never write to an organization's shared inbox (info@, contact@ and the like): the email has to reach the person responsible for the matter. If the person's listed channel is a contact form, use the form.

B2B contact databases (Apollo, Hunter, RocketReach, Lusha and similar) can help confirm a pattern. Use them only through an account the user already has and check their current terms; don't create accounts or enter credentials on the user's behalf.

Don't take addresses from places people didn't publish them for contact, such as the author metadata of public git commits or leaked lists.

## 4. Check relevance before drafting

Look at the candidate's recent public, professional activity (roughly the last three months: posts, talks, papers, press) to confirm two things:

1. They still hold the role. Profiles go stale.
2. The proposal intersects with their stated priorities or the metrics they're responsible for.

Stay within public, professional information. Don't collect anything about their private life, and don't build a profile beyond what the email needs. Every fact you plan to mention in the email gets its source link in the table; the drafting step checks it against that page again.

## Output: the candidate table

| Name | Title | Organization | Why this person (source link) | Contact (source; published or inferred) | Role checked on |
|---|---|---|---|---|---|

Show the table to the user and wait for them to choose before drafting. Then continue with the main `reach-out` flow.

## Limits

- This is for one-to-one, relevant, low-volume outreach, not bulk campaigns.
- Rules on unsolicited commercial email differ by country: some require prior or implied consent, and most require an easy way to opt out. If the recipient's country is unclear, tell the user before sending.
- Anyone who declines, or asks not to be contacted, goes on the do-not-contact list in `settings.md`.
