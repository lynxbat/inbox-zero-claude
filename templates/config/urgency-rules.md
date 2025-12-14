# Urgency Rules

Configuration for email urgency scoring during inbox triage.

## VIP Senders (always 🔴)

- CEO / Executive team members
- Direct manager
- Key stakeholders (customize this list)

## Keyword Triggers

### 🔴 Urgent Keywords (in subject)
- urgent
- ASAP
- EOD
- action required
- deadline
- immediate
- critical
- escalation

### 🟡 Attention Keywords (in subject)
- FYI
- update
- reminder
- follow-up
- review needed
- please review

### ⚪ Routine Keywords (in subject)
- newsletter
- digest
- automated
- no reply needed
- weekly update

## Age Rules

- >5 days in inbox → 🟡 (needs attention)
- >10 days in inbox → 🔴 (overdue)

## Program Priority Boosts

Programs with elevated visibility get +1 urgency level:

- Major launches (board/exec visibility)
- Go-live projects (timeline risk)
- Customer-impacting initiatives

## Auto-Archive Rules

Emails that should auto-archive unless explicitly tagged:

- CC'd on operational threads (not directly addressed)
- Routine status updates
- Automated system notifications
- Team-wide announcements (read and archive)

## Auto-Delete Rules

Emails that should always be deleted (noise):

- Marketing newsletters you never read
- Outdated notification types

## Auto-File Rules

Emails that should auto-file to specific folders:

- Confluence/wiki digests → relevant project folder
- CI/CD notifications → Engineering
- Expense reports → Corporate/Finance

## Auto-Analyze Rules

Emails with attachments that trigger analysis pipeline:

- **Daily Sales Reports** from reports@company.com
  - Subject: "Daily Sales Report"
  - Attachment: Excel/PDF
  - Action: Save to `attachments/DailySales/`, generate analysis
  - Output: `~/Reports/daily_sales_analysis.pdf`

- **Weekly Metrics** from analytics@company.com
  - Subject: "Weekly Metrics"
  - Attachment: Excel
  - Action: Save to `attachments/WeeklyMetrics/`

## Learned Adjustments

*Rules added during triage sessions:*

<!-- Append new learnings here with date -->
<!-- Example:
- 2025-01-15: Auto-archive CC'd operational emails unless called out
- 2025-01-20: Marketing weekly digest → auto-archive
-->
