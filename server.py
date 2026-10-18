import sqlite3
from datetime import datetime, date as date_cls
from mcp.server.fastmcp import FastMCP
import database
from database import create_database

mcp=FastMCP('Smart Expense Tracker MCP')
create_database()

def get_conn():
    return sqlite3.connect(database.DB_PATH)

def current_month():
    return date_cls.today().strftime('%Y-%m')

def check_month(month):
    if not month:
        return current_month()
    try: 
        datetime.strptime(month, '%Y-%m')
    except ValueError:
        raise ValueError('Month must be in YYYY-MM format, e.g. 2026-10')
    return month

@mcp.tool()
def add_expense(title:str, amount:float, category:str, date:str='')-> str:
    if not title.strip():
        raise ValueError('Title cannot be empty')
    if not category.strip():
        raise ValueError('Category cannot be empty')
    if amount <=0:
        raise ValueError('Amount must be greater than 0')
    if not date:
        date=date_cls.today().isoformat()
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Date must be in YYYY-MM-DD format, e.g. 2026-10-18')
    
    conn=get_conn()
    conn.execute('INSERT INTO expenses (title, amount, category, date) VALUES (?,?,?,?)',
                   (title.strip(), amount, category.strip().lower(), date))
    conn.commit()
    conn.close()
    return f'Expense "{title.strip()}" of Rs.{amount} added under {category.strip().lower()} on {date}'

@mcp.tool()
def monthly_total(month:str='')->str:
    month=check_month(month)
    conn=get_conn()
    total=conn.execute('SELECT SUM(amount) FROM expenses WHERE date LIKE?', (month + '%',)).fetchone()[0]
    conn.close()
    return f'Total Expenses for {month}: Rs.{total or 0}'

@mcp.tool()
def top_categories(month:str='', limit:int=3)->str:
    month=check_month(month)
    if limit < 1 or limit > 10:
        raise ValueError('Limit must be between 1 and 10')
    conn=get_conn()
    rows=conn.execute('''SELECT category, SUM(amount) AS total FROM expenses WHERE date LIKE? GROUP BY category ORDER BY total DESC LIMIT?''',(month + '%', limit)).fetchall()
    conn.close()
    if not rows:
        return f'No expenses found for {month}' 
    lines=[f'{i}.{cat}: Rs.{total}' for i, (cat, total) in enumerate(rows, 1)]
    return f'Top categories for {month}:\n'+'\n'.join(lines)

@mcp.resource('expense://monthly_report')
def monthly_report()->str:
    month=current_month()
    conn=get_conn()
    rows=conn.execute('SELECT date, title, category, amount FROM expenses WHERE date LIKE? ORDER BY date' , (month + '%',)).fetchall()
    conn.close()
    if not rows:
        return f'No expenses recorded for {month}'
    lines=[f'{d}|{t}|{c}|Rs.{a}' for d,t,c,a in rows]
    return f'Expense report for {month}\n' + '\n'.join(lines)

@mcp.prompt()
def budget_summary()->str:
    return (
        'You are an AI Expense Tracking Assistant.\n'
        '1. Call monthly_total for the current month and show the total spending.\n'
        '2. Call top_categories and identify the highest spending category.\n'
        '3. Suggest 2 ways to reduce unnecessary expenses.\n'
        '4. Provide a simple monthly budget plan.\n'
        'Always respond in a short, clear and professional manner.'
    )

if __name__=='__main__':
    mcp.run()