# Inbox Zero Claude

Email organization and triage workflow powered by Claude Code.

## Prerequisites

- [outlook-mcp](https://github.com/lynxbat/claude-outlook-mcp) configured in Claude Code
- Microsoft Outlook for macOS

## Quick Start

1. Copy templates to create your config:
   ```bash
   cp -r templates/config logs/config
   cp -r templates/people logs/people
   cp -r templates/topics logs/topics
   cp -r templates/companies logs/companies
   cp -r templates/programs logs/programs
   mkdir -p attachments
   ```

2. Edit `logs/config/` files with your rules

3. Run `/inbox-zero` to start triage

## Email Organization

**Before organizing emails, read these config files:**
- `logs/config/folder-sorting-rules.md` - Vendor classification, sender rules
- `logs/config/urgency-rules.md` - VIP senders, urgency keywords
- `logs/config/send-permissions.md` - Draft vs auto-send rules

**Key Principles:**
- Archive is ONLY for truly irrelevant emails
- All business emails belong in a categorized folder
- VIP emails always surface for review

## File Organization

**Attachments:** `attachments/`
- Email attachments saved here for analysis
- Organized by topic subfolder

**Logs:** `logs/`
- `config/` - Your sorting and urgency rules
- `people/` - Person-specific context and history
- `topics/` - Topic/thread tracking
- `companies/` - Vendor context
- `programs/` - Program tracking

**Reports:** `~/Reports/inbox-zero/`
- Generated analysis reports (PDF)

## Cache

The email cache at `email_cache.db` speeds up triage by storing email metadata locally.

To sync: `python scripts/email_cache.py sync`
To search: `python scripts/email_cache.py search <term>`

## Creating New Log Types

Add any folder under `logs/` for new context types. The inbox-zero workflow will read all markdown files in `logs/` subfolders.

Example: `logs/incidents/` for tracking incidents.
