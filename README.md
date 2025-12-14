# Inbox Zero for Claude

Achieve inbox zero with Claude Code. An intelligent email workflow that learns your organization patterns and helps you process email efficiently.

## What It Does

- **Triage emails** by urgency (VIPs, keywords, age)
- **Auto-categorize** by sender, domain, and content
- **File intelligently** based on your rules
- **Draft responses** following your preferences
- **Track context** about people, topics, and programs
- **Learn patterns** and improve over time

## Prerequisites

- [Claude Code](https://claude.ai/code) (CLI or IDE extension)
- A supported email provider (see below)

## Supported Email Providers

### Outlook for macOS (via outlook-mcp)

Currently, inbox-zero-claude works with **Microsoft Outlook for macOS** through the [outlook-mcp](https://github.com/lynxbat/claude-outlook-mcp) server.

> **Note:** This links to a fork with enhanced features. Once [PR #5](https://github.com/syedazharmbnr1/claude-outlook-mcp/pull/5) is merged, the upstream repo will be recommended.

#### What outlook-mcp provides

| Capability | Description |
|------------|-------------|
| **Read emails** | Fetch inbox, search, filter by date |
| **Send/Reply** | Compose and send emails (with HTML support) |
| **Organize** | Move to folders, archive, delete |
| **Folders** | Create, rename, list folders |
| **Attachments** | Save attachments to disk |
| **Calendar** | Read and create calendar events |
| **Contacts** | Search contacts |

#### Installation

1. **Install Bun** (if not already installed):
   ```bash
   curl -fsSL https://bun.sh/install | bash
   ```

2. **Clone outlook-mcp**:
   ```bash
   git clone https://github.com/lynxbat/claude-outlook-mcp.git
   cd claude-outlook-mcp
   bun install
   ```

3. **Grant Outlook permissions**:
   - Open Microsoft Outlook for macOS
   - When prompted, allow automation/accessibility permissions
   - outlook-mcp communicates with Outlook via AppleScript

4. **Add to Claude Code config** (`~/.claude.json`):
   ```json
   {
     "mcpServers": {
       "outlook-mcp": {
         "command": "bun",
         "args": ["run", "/path/to/claude-outlook-mcp/index.ts"]
       }
     }
   }
   ```

5. **Verify it works**:
   ```bash
   claude
   # Then ask: "List my recent emails"
   ```

#### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Outlook not responding" | Ensure Outlook is open and not in a modal dialog |
| Permission denied | Grant Terminal/Claude automation access in System Preferences → Privacy & Security |
| MCP not found | Check the path in `~/.claude.json` is correct |

### Other Providers (Future)

Gmail, IMAP, and other providers are not yet supported but the architecture allows for future expansion. Contributions welcome!

---

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/YOUR_USERNAME/inbox-zero-claude.git
cd inbox-zero-claude
```

### 2. Copy Templates to Create Your Config

```bash
cp -r templates/config logs/config
cp -r templates/people logs/people
cp -r templates/topics logs/topics
cp -r templates/companies logs/companies
cp -r templates/programs logs/programs
mkdir -p attachments
```

### 3. Configure Your Rules

Edit the files in `logs/config/`:

- **`folder-sorting-rules.md`** - Define vendors, sender rules, keyword mappings
- **`urgency-rules.md`** - Set VIP senders, urgent keywords, auto-archive rules
- **`send-permissions.md`** - Control when Claude can send vs draft

### 4. Install Email Provider

Follow the [outlook-mcp installation](#installation) instructions above.

### 5. Run Inbox Zero

In Claude Code, navigate to this project and run:

```
/inbox-zero
```

## How It Works

### Two-Pass Triage

**Pass 1: Quick Scan**
- Syncs new emails to local cache
- Scores each email by urgency (🔴 🟡 ⚪)
- Presents a summary table for review

**Pass 2: Conversational Processing**
- Works through emails one at a time
- Presents context from your logs
- You decide: respond, file, archive, delete, defer, delegate
- Claude executes and updates logs

### Context System

The `logs/` folder stores your personalized context:

| Folder | Purpose |
|--------|---------|
| `config/` | Sorting rules, urgency settings, send permissions |
| `people/` | Notes about individuals you email with |
| `topics/` | Tracking for ongoing threads/topics |
| `companies/` | Vendor and company context |
| `programs/` | Project and program tracking |

Context builds over time as you triage, making Claude smarter about your email.

### Email Cache

A local SQLite cache (`email_cache.db`) speeds up triage:

```bash
python scripts/email_cache.py sync      # Sync new emails
python scripts/email_cache.py search <term>  # Search cache
python scripts/email_cache.py stats     # Cache statistics
```

## Configuration Guide

### Folder Sorting Rules

Define where emails should be filed:

```markdown
## Vendor Classification

| Vendor | Domain | Folder |
|--------|--------|--------|
| Stripe | stripe.com | Payments/Stripe |
| AWS | amazon.com | Cloud/AWS |

## Sender Rules

| Sender | Target Folder |
|--------|---------------|
| *@github.com | Engineering |
| reports@* | Analytics |
```

### Urgency Rules

Control what gets flagged:

```markdown
## VIP Senders (always 🔴)
- ceo@company.com
- manager@company.com

## Urgent Keywords
- urgent, ASAP, critical, deadline

## Auto-Archive
- newsletters, digests, "out of office"
```

### Send Permissions

Protect against accidental sends:

```markdown
## Always Draft (Never Auto-Send)
- External vendors
- Executives
- Budget discussions
- First-time contacts
```

## Project Structure

```
inbox-zero-claude/
├── templates/          # Example configs (public)
│   ├── config/
│   ├── people/
│   ├── topics/
│   ├── companies/
│   └── programs/
├── logs/               # Your configs (gitignored)
├── attachments/        # Saved attachments (gitignored)
├── scripts/            # Python utilities
├── .claude/commands/   # Slash commands
├── CLAUDE.md           # Project instructions
└── README.md
```

## Extending

### Add New Log Types

Create any folder under `logs/` for new context types:

```bash
mkdir logs/incidents
mkdir logs/vendors
```

The inbox-zero workflow reads all markdown files in `logs/` subfolders.

### Custom Analyzers

Add Python scripts to `scripts/` for custom email analysis:

```python
# scripts/my_analyzer.py
# Triggered by urgency-rules.md auto-analyze rules
```

## License

MIT
