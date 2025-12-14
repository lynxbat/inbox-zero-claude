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

### Compatibility Matrix

| Provider | Platform | MCP | Status |
|----------|----------|-----|--------|
| **Outlook (Legacy)** | macOS | [outlook-mcp](https://github.com/lynxbat/claude-outlook-mcp) | ✅ Supported |
| **Outlook (New)** | macOS | — | ❌ Not supported (no AppleScript) |
| **Outlook** | Windows | — | ❌ Not tested |
| **Microsoft 365** | Web/API | — | 🔮 Wishlist |
| **Gmail** | All | See wishlist | 🔮 Wishlist |
| **IMAP/SMTP** | All | See wishlist | 🔮 Wishlist |
| **Apple Mail** | macOS | — | 🔮 Wishlist |

> **Note:** "Outlook (Legacy)" refers to the traditional Outlook for Mac app, not the newer web-based "New Outlook" which doesn't support AppleScript automation.

### Email MCP Wishlist

These MCPs exist in the ecosystem and could potentially be integrated:

| MCP | Protocol | Notes |
|-----|----------|-------|
| [Gmail-MCP-Server](https://github.com/GongRzhe/Gmail-MCP-Server) | Gmail API | OAuth authentication, full Gmail integration |
| [imap-mcp-server](https://github.com/nikolausm/imap-mcp-server) | IMAP/SMTP | Works with Gmail, Outlook.com, Yahoo, 15+ providers |
| [imap-mcp](https://github.com/non-dirty/imap-mcp) | IMAP | Interactive email processing, learns preferences |
| [Universal Email](https://www.pulsemcp.com/servers/timecyber-universal-email) | IMAP/POP3/SMTP | Auto-detects provider settings |

**Want to add support?** The inbox-zero workflow is MCP-agnostic. If an email MCP provides read, send, and organize capabilities, it should work with minimal changes to the `/inbox-zero` command. PRs welcome!

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

### Building Rules During Triage

As Claude presents emails, you can teach it your preferences by asking it to create rules. Here are examples:

**Sender & Domain Rules**
```
"Always file emails from @stripe.com to Payments/Stripe"
"Add sarah@vendor.com as a VIP"
"Emails from this domain should go to Engineering"
```

**Keyword Rules**
```
"Auto-archive anything with 'newsletter' in the subject"
"Flag emails mentioning 'deadline' or 'urgent' as high priority"
"Weekly digest emails should auto-file to Analytics"
```

**Pattern Rules**
```
"This sender always sends reports - file to Analytics/Reports"
"Meeting invites from this person are always 1:1s - file to People/John"
"Anything from *@noreply.* should be low priority"
```

**Context & People**
```
"Create a log for this person - they're my main contact at Acme"
"Start tracking this topic - it's a Q1 initiative"
"Add this company as a vendor under Payments"
```

**Adjusting Urgency**
```
"This type of email is never urgent - add to auto-archive"
"Emails from this sender should always be 🔴"
"Downgrade notifications from this service to ⚪"
```

Claude will update the appropriate config file (`folder-sorting-rules.md`, `urgency-rules.md`, etc.) and apply the rule going forward.

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
