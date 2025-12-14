---
description: Weekly email triage workflow for inbox zero
---

# Inbox Zero Triage

You are helping me achieve inbox zero through a two-pass triage workflow.

## First Run Detection

Before anything else, check if this is a first-time setup:

1. Check if `logs/config/folder-sorting-rules.md` exists
2. If **missing or empty** → Enter **Setup Mode** (see below)
3. If **exists** → Continue to normal triage workflow

---

## Setup Mode (First Run Only)

If logs/config doesn't exist, guide the user through initial setup:

### Step 1: Create Directory Structure

```bash
cp -r templates/config logs/config
cp -r templates/people logs/people
cp -r templates/topics logs/topics
cp -r templates/companies logs/companies
cp -r templates/programs logs/programs
mkdir -p attachments
```

### Step 2: Verify Outlook MCP

Test that outlook-mcp is configured:
- Try fetching 1 email from inbox
- If it fails, guide user to configure outlook-mcp

### Step 3: Analyze Inbox (Optional)

Ask: "Would you like me to analyze your recent emails to suggest personalized rules?"

If yes:
1. Fetch last 50-100 emails from inbox
2. Identify patterns:
   - **Top senders** → Suggest as VIPs or auto-file rules
   - **Common domains** → Suggest vendor classifications
   - **Existing Outlook folders** → Incorporate into folder rules
3. Present findings and let user approve/modify
4. Update `logs/config/` files with personalized rules

If no:
- User can edit templates manually later

### Step 4: Confirm Ready

Say: "Setup complete! Your config is in `logs/config/`. Run `/inbox-zero` again to start triaging."

Exit setup mode.

---

## Normal Triage Mode

### Context Loading Phase

Before starting triage, load context:

1. Read all files in `logs/config/` for urgency rules and send permissions
2. Read all files in `logs/people/` for sender context
3. Read all files in `logs/companies/` for vendor/firm context
4. Read all files in `logs/programs/` for program context
5. Read all files in `logs/topics/` for topic context

If any logs directory is empty, that's fine - we'll create logs as we go.

## Cache Sync Phase

The email cache lives at `email_cache.db`. Before triage:

1. Check the most recent email date in the cache:
   ```sql
   SELECT MAX(date) FROM emails WHERE folder = 'Inbox'
   ```
2. Fetch any new emails from Outlook since that date using date filter
3. Insert new emails into the cache
4. Report sync status: "Cache synced: X new emails added"

Use the cache for triage queries - only hit Outlook MCP for:
- Syncing new emails
- Reading full email content when processing
- Executing actions (archive, move, send)

## Pass 1: Quick Scan

1. Query the cache for all Inbox emails (newest first)
2. For each email, score urgency based on rules in `logs/config/urgency-rules.md`:
   - Check if sender is VIP → 🔴
   - Check subject for urgent keywords → 🔴
   - Check subject for attention keywords → 🟡
   - Check age (>5 days = 🟡, >10 days = 🔴)
   - Check if related to priority programs → boost urgency
   - Use AI judgment on content for time-sensitivity
3. Cross-reference senders/topics with existing logs for additional context
4. Present a summary table:

```
## Inbox Triage - [DATE] ([COUNT] emails)

| # | Urgency | From | Subject | Context |
|---|---------|------|---------|---------|
| 1 | 🔴 | ... | ... | ... |
```

5. Ask: "Ready to process? Any flags to adjust first?"

## Pass 2: Conversational Processing

Work through emails starting with 🔴, then 🟡, then ⚪.

For each email:

1. **Present** the email with:
   - Full content summary
   - Any relevant context from logs
   - Your assessment of what's being asked/needed

2. **Discuss** with me:
   - What's the right response (if any)?
   - Any context I should know?

3. **I choose an action:**
   - **Respond** - You draft a reply, then ask "Send now, or open as draft?"
   - **File** - You suggest a folder or I name a new one, then move it
   - **Archive** - Move to Archive folder
   - **Delete** - Delete from Outlook
   - **Defer** - Flag for follow-up, I specify when
   - **Delegate** - You draft a forward with context, I specify recipient

4. **Execute** the action using Outlook MCP

5. **Update logs:**
   - Append decision to relevant people/company/program logs
   - If new sender/topic, ask if I want to create a new log
   - If I adjusted urgency, add rule to urgency-rules.md

6. **Move to next email**

## Folder Management

- Refer to `logs/config/folder-sorting-rules.md` for existing structure
- Create new Outlook folders as patterns emerge
- I approve all new folder names

## After Processing

Summarize the session:
- Total emails processed
- Breakdown by action (X responded, X filed, X archived, etc.)
- New logs created
- New urgency rules added

Ask: "Want me to commit these log updates?"

## Important Notes

- Always ask before sending any email response
- One email at a time, conversational style
- If Outlook sync is incomplete, use search as fallback
- If I want to stop mid-session, that's fine - we pick up next time
