import html
from typing import Dict, List, Any, Optional
import pandas as pd
import streamlit as st
import sqlglot
from sqlglot import exp

SCHEMA_METADATA: Dict[str, Dict[str, Any]] = {
    "customers": {
        "role": "Client identity, city & KYC risk profile",
        "pk": "customer_id",
        "columns": [
            {"name": "customer_id", "type": "INTEGER", "key": "PK"},
            {"name": "full_name", "type": "TEXT", "key": None},
            {"name": "city", "type": "TEXT", "key": None},
            {"name": "risk_tier", "type": "TEXT", "key": None},
            {"name": "kyc_verified", "type": "INTEGER", "key": None},
            {"name": "signup_date", "type": "DATE", "key": None},
        ],
    },
    "accounts": {
        "role": "Deposit & corporate ledger balances (PKR)",
        "pk": "account_id",
        "columns": [
            {"name": "account_id", "type": "INTEGER", "key": "PK"},
            {"name": "customer_id", "type": "INTEGER", "key": "FK → customers"},
            {"name": "account_type", "type": "TEXT", "key": None},
            {"name": "balance_pkr", "type": "REAL", "key": None},
            {"name": "status", "type": "TEXT", "key": None},
        ],
    },
    "transactions": {
        "role": "Double-entry transfers & real-time fraud flags",
        "pk": "txn_id",
        "columns": [
            {"name": "txn_id", "type": "INTEGER", "key": "PK"},
            {"name": "account_id", "type": "INTEGER", "key": "FK → accounts"},
            {"name": "merchant_id", "type": "INTEGER", "key": "FK → merchants"},
            {"name": "amount_pkr", "type": "REAL", "key": None},
            {"name": "txn_type", "type": "TEXT", "key": None},
            {"name": "is_flagged_fraud", "type": "INTEGER", "key": None},
            {"name": "txn_timestamp", "type": "DATETIME", "key": None},
        ],
    },
    "merchants": {
        "role": "Commercial vendors & settlement categories",
        "pk": "merchant_id",
        "columns": [
            {"name": "merchant_id", "type": "INTEGER", "key": "PK"},
            {"name": "merchant_name", "type": "TEXT", "key": None},
            {"name": "category", "type": "TEXT", "key": None},
            {"name": "city", "type": "TEXT", "key": None},
        ],
    },
    "loans": {
        "role": "Credit principal exposure & default status",
        "pk": "loan_id",
        "columns": [
            {"name": "loan_id", "type": "INTEGER", "key": "PK"},
            {"name": "customer_id", "type": "INTEGER", "key": "FK → customers"},
            {"name": "principal_pkr", "type": "REAL", "key": None},
            {"name": "interest_rate", "type": "REAL", "key": None},
            {"name": "loan_status", "type": "TEXT", "key": None},
        ],
    },
}


def render_wordmark_header():
    st.markdown("""
    <div class="qf-header-row">
        <div class="qf-wordmark">
            <span class="qf-wordmark-name">QueryForge</span>
            <span class="qf-wordmark-meta">Qwen2.5-Coder-1.5B · QLoRA · sqlglot</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_editorial_hero(kicker: str, title: str, lead: str):
    st.markdown(f"""
    <div class="qf-hero">
        <span class="qf-kicker">{html.escape(kicker)}</span>
        <h1 class="qf-display-title">{html.escape(title)}</h1>
        <p class="qf-lead-copy">{html.escape(lead)}</p>
    </div>
    """, unsafe_allow_html=True)


def format_sql_pretty(sql_query: str) -> str:
    try:
        return sqlglot.transpile(sql_query, read="sqlite", write="sqlite", pretty=True)[0] + ";"
    except Exception:
        return sql_query


def extract_ast_clauses(sql_query: str) -> List[Dict[str, str]]:
    clauses = []
    try:
        parsed = sqlglot.parse_one(sql_query, read="sqlite")
        if parsed.find(exp.Select):
            select_exprs = [e.sql() for e in parsed.expressions[:6]]
            clauses.append({"node": "SELECT", "detail": ", ".join(select_exprs)})
        from_node = parsed.find(exp.From)
        if from_node:
            clauses.append({"node": "FROM", "detail": from_node.sql()})
        for j in parsed.find_all(exp.Join):
            clauses.append({"node": "JOIN", "detail": j.sql()})
        where_node = parsed.find(exp.Where)
        if where_node:
            clauses.append({"node": "WHERE", "detail": where_node.sql()})
        group_node = parsed.find(exp.Group)
        if group_node:
            clauses.append({"node": "GROUP BY", "detail": group_node.sql()})
        having_node = parsed.find(exp.Having)
        if having_node:
            clauses.append({"node": "HAVING", "detail": having_node.sql()})
        order_node = parsed.find(exp.Order)
        if order_node:
            clauses.append({"node": "ORDER BY", "detail": order_node.sql()})
    except Exception as e:
        clauses.append({"node": "PARSE_ERROR", "detail": str(e)})
    return clauses


def render_schema_grounding_chapter(active_tables: List[str]):
    all_tables = ["customers", "accounts", "transactions", "merchants", "loans"]
    items_html = ""
    for t in all_tables:
        is_active = t in active_tables
        cls = "active" if is_active else "inactive"
        dot = "●" if is_active else "○"
        items_html += f'<span class="qf-entity-item {cls}">{dot} {t}</span>'

    st.markdown(f"""
    <div class="qf-chapter">
        <div class="qf-chapter-meta">
            <span><span class="qf-chapter-num">01</span> &nbsp;Schema Context Grounding</span>
            <span>{len(active_tables)} of 5 tables selected for prompt conditioning</span>
        </div>
        <div class="qf-entity-strip">
            {items_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_generated_sql_chapter(sql_query: str, ast_info: Dict[str, Any], healed_used: bool):
    pretty_sql = format_sql_pretty(sql_query)
    valid_text = "✓ SQL valid · AST verified · Read-only safe" if ast_info["is_valid"] else "✕ AST syntax violation"
    path_text = " → ".join(ast_info["tables"]) if ast_info["tables"] else "single table"
    heal_note = '<span class="qf-status-warn">↻ Zero-shot draft repaired via compiler feedback</span>' if healed_used else ""

    st.markdown(f"""
    <div class="qf-chapter">
        <div class="qf-chapter-meta">
            <span><span class="qf-chapter-num">02</span> &nbsp;Synthesized SQL</span>
            <span>Join path: {html.escape(path_text)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.code(pretty_sql, language="sql", line_numbers=True)

    st.markdown(f"""
    <div class="qf-validation-strip">
        <span class="qf-status-ok">{valid_text}</span>
        {heal_note}
    </div>
    """, unsafe_allow_html=True)


def render_self_correction_rail(base_error: str, heal_reason: str):
    st.markdown(f"""
    <div class="qf-correction-rail">
        <div class="qf-rail-step">
            <span class="qf-rail-tag" style="color:#8C857B;">Step 1</span>
            <div class="qf-rail-title">Generated</div>
            <div class="qf-rail-note">Zero-shot base model emitted initial SQL.</div>
        </div>
        <div class="qf-rail-step">
            <span class="qf-rail-tag" style="color:#B91C1C;">Step 2 · Failed</span>
            <div class="qf-rail-title">Compiler Error</div>
            <div class="qf-rail-note">{html.escape(base_error[:58])}</div>
        </div>
        <div class="qf-rail-step">
            <span class="qf-rail-tag" style="color:#B45309;">Step 3 · Corrected</span>
            <div class="qf-rail-title">Schema Repair</div>
            <div class="qf-rail-note">{html.escape(heal_reason[:64])}</div>
        </div>
        <div class="qf-rail-step">
            <span class="qf-rail-tag" style="color:#1E40AF;">Step 4</span>
            <div class="qf-rail-title">Validated</div>
            <div class="qf-rail-note">AST verified against SQLite DDL.</div>
        </div>
        <div class="qf-rail-step">
            <span class="qf-rail-tag" style="color:#15803D;">Step 5</span>
            <div class="qf-rail-title">Executed</div>
            <div class="qf-rail-note">Returned verified rows cleanly.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_editorial_results(df: pd.DataFrame, elapsed_ms: int):
    row_count = len(df)
    cols = list(df.columns)
    thead = "".join(f"<th>{html.escape(str(c))}</th>" for c in cols)
    rows_html = ""
    for _, r in df.head(30).iterrows():
        cells = ""
        for c in cols:
            val = r[c]
            txt = f"{val:,.2f}" if isinstance(val, float) else str(val)
            cells += f"<td>{html.escape(txt)}</td>"
        rows_html += f"<tr>{cells}</tr>"

    st.markdown(f"""
    <div class="qf-chapter">
        <div class="qf-chapter-meta">
            <span><span class="qf-chapter-num">03</span> &nbsp;Execution Result</span>
            <span>fintech_ledger.db · SQLite3</span>
        </div>
        <div class="qf-result-header">
            <h2 class="qf-result-title">Query Complete <span style="color:#15803D;">✓</span></h2>
            <div class="qf-result-stats">{row_count} rows · {elapsed_ms}ms</div>
        </div>
        <div class="qf-table-scroll">
            <table class="qf-editorial-table">
                <thead><tr>{thead}</tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_architectural_schema_map(selected_table: Optional[str] = None):
    """Precision SVG blueprint showing relational tables and foreign-key pathways."""
    adjacency = {
        "customers": {"customers", "accounts", "loans"},
        "accounts": {"accounts", "customers", "transactions"},
        "transactions": {"transactions", "accounts", "merchants"},
        "merchants": {"merchants", "transactions"},
        "loans": {"loans", "customers"},
    }
    active_set = adjacency.get(selected_table, {"customers", "accounts", "transactions", "merchants", "loans"})

    def entity_node(t_id: str, x: int, y: int, label: str, pk: str, sub: str):
        is_on = t_id in active_set
        stroke = "#1E40AF" if is_on else "#D6D3C9"
        stroke_w = "2" if is_on else "1.2"
        fill = "#FFFFFF" if is_on else "#FAF9F6"
        title_col = "#141413" if is_on else "#8C857B"
        pk_col = "#1E40AF" if is_on else "#A8A29E"
        return f"""
        <g transform="translate({x},{y})">
            <rect x="-102" y="-38" width="204" height="76" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}" />
            <text x="0" y="-10" text-anchor="middle" fill="{title_col}" font-family="Inter, sans-serif" font-size="13" font-weight="600">{label}</text>
            <text x="0" y="9" text-anchor="middle" fill="{pk_col}" font-family="JetBrains Mono, monospace" font-size="10.5">{pk}</text>
            <text x="0" y="25" text-anchor="middle" fill="#78716C" font-family="JetBrains Mono, monospace" font-size="9.5">{sub}</text>
        </g>
        """

    def edge_line(t1: str, t2: str, d: str, lx: int, ly: int, key_name: str):
        is_on = (t1 in active_set) and (t2 in active_set)
        col = "#1E40AF" if is_on else "#D6D3C9"
        w = "1.8" if is_on else "1.1"
        dash = 'stroke-dasharray="6 4" style="animation: tracePulse 1.8s linear infinite;"' if is_on else ""
        txt_col = "#1E40AF" if is_on else "#A8A29E"
        return f"""
        <path d="{d}" stroke="{col}" stroke-width="{w}" {dash} fill="none" />
        <text x="{lx}" y="{ly}" text-anchor="middle" fill="{txt_col}" font-family="JetBrains Mono, monospace" font-size="9.5">{key_name}</text>
        """

    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #E2DFD7; border-radius:14px; padding:1.25rem; margin:1.25rem 0 2rem 0;">
        <svg viewBox="0 0 880 300" width="100%" height="280" style="display:block; margin:0 auto;">
            {edge_line("customers", "accounts", "M 252 80 L 338 80", 295, 70, "customer_id")}
            {edge_line("accounts", "transactions", "M 542 80 L 628 80", 585, 70, "account_id")}
            {edge_line("customers", "loans", "M 150 118 L 245 192", 175, 165, "customer_id")}
            {edge_line("merchants", "transactions", "M 635 192 L 730 118", 705, 165, "merchant_id")}

            {entity_node("customers", 150, 80, "customers", "PK: customer_id", "city · risk_tier · kyc")}
            {entity_node("accounts", 440, 80, "accounts", "PK: account_id", "FK: customer_id · balance_pkr")}
            {entity_node("transactions", 730, 80, "transactions", "PK: txn_id", "FK: account_id, merchant_id")}
            {entity_node("loans", 285, 230, "loans", "PK: loan_id", "FK: customer_id · loan_status")}
            {entity_node("merchants", 595, 230, "merchants", "PK: merchant_id", "category · city")}
        </svg>
    </div>
    """, unsafe_allow_html=True)
