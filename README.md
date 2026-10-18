# Smart Expense Tracker MCP

## Overview

An MCP server that lets an AI app like Claude Desktop add expenses and answer questions about them. Data is stored in SQLite.

## MCP Parts

- Tools: add_expense, monthly_total, top_categories
- Resource: expense://monthly_report
- Prompt: budget_summary

## Setup

1. Install Python 3.10+ and Node.js 18+
2. Create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install packages:

```bash
pip install -r requirements.txt
```

4. Test with MCP Inspector:

```bash
mcp dev server.py
```

## Connect to Claude Desktop

Open Settings > Developer > Edit Config and add:

```json
{
  "mcpServers": {
    "expense-tracker": {
      "command": "C:/full/path/to/venv/Scripts/python.exe",
      "args": ["C:/full/path/to/server.py"]
    }
  }
}
```

Restart Claude Desktop.

## Example Questions

- I spent 250 on food today, add it
- What is my total expense this month?
- Which category did I spend the most on?

## Run Tests

```bash
pytest
```

## Error Handling

Wrong input returns a clear message. For example: negative amount, empty title, wrong date format (use YYYY-MM-DD) or wrong month format (use YYYY-MM).

## Future Enhancements

- Monthly charts
- Export reports to PDF and Excel
- Edit and delete expenses

