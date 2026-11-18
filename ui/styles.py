import streamlit as st

def inject_editorial_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
            --bg-paper: #F6F5F1;
            --bg-surface: #FFFFFF;
            --bg-subtle: #EFECE6;
            --bg-code: #181817;
            --ink-primary: #141413;
            --ink-secondary: #57534E;
            --ink-muted: #8C857B;
            --rule-hairline: #E2DFD7;
            --rule-strong: #C9C4B8;
            --accent-cobalt: #1E40AF;
            --accent-cobalt-soft: rgba(30, 64, 175, 0.08);
            --status-ok: #15803D;
            --status-ok-bg: rgba(21, 128, 61, 0.08);
            --status-err: #B91C1C;
            --status-err-bg: rgba(185, 28, 28, 0.07);
            --status-warn: #B45309;
            --status-warn-bg: rgba(180, 83, 9, 0.08);
        }

        /* Remove Streamlit admin chrome & sidebar completely */
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        #MainMenu,
        footer {
            display: none !important;
        }

        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: var(--bg-paper) !important;
            color: var(--ink-primary) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            -webkit-font-smoothing: antialiased;
        }

        /* Generous, calm reading & working column */
        .block-container {
            max-width: 920px !important;
            padding-top: 1.75rem !important;
            padding-bottom: 6rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            margin: 0 auto !important;
        }

        @keyframes subtleReveal {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes tracePulse {
            to {
                stroke-dashoffset: -36;
            }
        }

        /* Minimal Architectural Header & Navigation */
        .qf-header-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 1.1rem;
            border-bottom: 1px solid var(--rule-hairline);
            margin-bottom: 2.2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .qf-wordmark {
            display: flex;
            align-items: baseline;
            gap: 0.65rem;
        }
        .qf-wordmark-name {
            font-family: 'Newsreader', Georgia, serif;
            font-size: 1.45rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--ink-primary);
        }
        .qf-wordmark-meta {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            color: var(--ink-muted);
            letter-spacing: 0.03em;
        }

        /* Restyle horizontal radio into clean editorial text tabs */
        div[role="radiogroup"] {
            display: flex !important;
            justify-content: flex-end !important;
            align-items: center !important;
            gap: 1.75rem !important;
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin: -3.55rem 0 2.5rem auto !important;
            width: fit-content !important;
        }
        div[role="radiogroup"] > label {
            background: transparent !important;
            border: none !important;
            border-bottom: 2px solid transparent !important;
            border-radius: 0 !important;
            padding: 0.35rem 0.1rem !important;
            margin: 0 !important;
            transition: border-color 0.2s ease, color 0.2s ease !important;
            cursor: pointer !important;
        }
        div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }
        div[role="radiogroup"] > label p {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            color: var(--ink-secondary) !important;
            margin: 0 !important;
        }
        div[role="radiogroup"] > label:hover p {
            color: var(--ink-primary) !important;
        }
        div[role="radiogroup"] > label[data-checked="true"],
        div[role="radiogroup"] > label:has(input:checked) {
            border-bottom: 2px solid var(--ink-primary) !important;
        }
        div[role="radiogroup"] > label[data-checked="true"] p,
        div[role="radiogroup"] > label:has(input:checked) p {
            color: var(--ink-primary) !important;
            font-weight: 600 !important;
        }

        /* Editorial Hero Focal Point */
        .qf-hero {
            padding: 1.25rem 0 2.25rem 0;
            animation: subtleReveal 0.45s ease both;
        }
        .qf-kicker {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            color: var(--accent-cobalt);
            margin-bottom: 0.85rem;
            display: block;
        }
        .qf-display-title {
            font-family: 'Newsreader', Georgia, serif !important;
            font-size: clamp(2.5rem, 4.8vw, 3.75rem) !important;
            font-weight: 500 !important;
            line-height: 1.08 !important;
            letter-spacing: -0.03em !important;
            color: var(--ink-primary) !important;
            margin: 0 0 1rem 0 !important;
        }
        .qf-lead-copy {
            font-size: 1.08rem !important;
            line-height: 1.6 !important;
            color: var(--ink-secondary) !important;
            max-width: 640px;
            margin: 0 !important;
            font-weight: 400;
        }

        /* Tactile White Command Input Surface */
        div[data-testid="stTextArea"] label {
            display: none !important;
        }
        div[data-testid="stTextArea"] textarea {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--rule-strong) !important;
            border-radius: 14px !important;
            padding: 1.25rem 1.4rem !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1.15rem !important;
            font-weight: 400 !important;
            line-height: 1.55 !important;
            color: var(--ink-primary) !important;
            box-shadow: 0 10px 30px -12px rgba(20, 20, 19, 0.08) !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        div[data-testid="stTextArea"] textarea:focus {
            border-color: var(--accent-cobalt) !important;
            box-shadow: 0 0 0 3px var(--accent-cobalt-soft), 0 14px 36px -12px rgba(20, 20, 19, 0.1) !important;
        }

        /* Primary Ink Button */
        button[kind="primary"] {
            background-color: var(--ink-primary) !important;
            color: #FFFFFF !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
            padding: 0.65rem 1.4rem !important;
            border-radius: 10px !important;
            border: 1px solid var(--ink-primary) !important;
            box-shadow: 0 2px 8px rgba(20, 20, 19, 0.12) !important;
            transition: background-color 0.15s ease, transform 0.15s ease !important;
        }
        button[kind="primary"]:hover {
            background-color: #292927 !important;
            transform: translateY(-1px) !important;
        }

        /* Quiet Suggestion Buttons */
        button[kind="secondary"] {
            background-color: transparent !important;
            border: 1px solid var(--rule-hairline) !important;
            color: var(--ink-secondary) !important;
            border-radius: 8px !important;
            font-size: 0.8rem !important;
            font-weight: 400 !important;
            padding: 0.38rem 0.75rem !important;
            transition: all 0.15s ease !important;
        }
        button[kind="secondary"]:hover {
            background-color: var(--bg-surface) !important;
            border-color: var(--rule-strong) !important;
            color: var(--ink-primary) !important;
        }

        /* Editorial Section Dividers (Replacing Card Boxes) */
        .qf-chapter {
            border-top: 1px solid var(--rule-hairline);
            padding-top: 2rem;
            margin-top: 2.25rem;
            animation: subtleReveal 0.45s ease both;
        }
        .qf-chapter-meta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.73rem;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: var(--ink-muted);
            margin-bottom: 0.85rem;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .qf-chapter-num {
            color: var(--ink-primary);
            font-weight: 600;
        }

        /* Schema Entity Strip (Typography + Subtle State, No Heavy Boxes) */
        .qf-entity-strip {
            display: flex;
            flex-wrap: wrap;
            gap: 1.25rem;
            align-items: center;
            padding: 0.5rem 0;
        }
        .qf-entity-item {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.84rem;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding-bottom: 0.25rem;
            transition: opacity 0.2s ease;
        }
        .qf-entity-item.active {
            color: var(--ink-primary);
            font-weight: 600;
            border-bottom: 2px solid var(--accent-cobalt);
        }
        .qf-entity-item.inactive {
            color: var(--ink-muted);
            opacity: 0.48;
            border-bottom: 2px solid transparent;
        }

        /* Matte Carbon SQL Code Block (Intentional Contrast Artifact) */
        div[data-testid="stCodeBlock"] pre {
            background-color: var(--bg-code) !important;
            color: #F4F4F2 !important;
            border: 1px solid #2C2C2A !important;
            border-radius: 12px !important;
            padding: 1.35rem 1.5rem !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.96rem !important;
            line-height: 1.65 !important;
            box-shadow: 0 12px 32px -12px rgba(20, 20, 19, 0.22) !important;
        }

        /* Quiet Status Line Below SQL */
        .qf-validation-strip {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 0.65rem;
            font-size: 0.84rem;
            color: var(--ink-secondary);
        }
        .qf-status-ok {
            color: var(--status-ok);
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }
        .qf-status-warn {
            color: var(--status-warn);
            font-weight: 500;
        }

        /* Self-Correction Horizontal Pipeline Timeline (No Card Grid) */
        .qf-correction-rail {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 0.75rem;
            padding: 1.15rem 0;
            border-top: 1px solid var(--rule-hairline);
            border-bottom: 1px solid var(--rule-hairline);
            margin: 1rem 0;
        }
        .qf-rail-step {
            padding-right: 0.5rem;
        }
        .qf-rail-tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
            display: block;
        }
        .qf-rail-title {
            font-size: 0.86rem;
            font-weight: 600;
            color: var(--ink-primary);
            margin-bottom: 0.2rem;
        }
        .qf-rail-note {
            font-size: 0.78rem;
            color: var(--ink-secondary);
            line-height: 1.4;
        }

        /* Editorial Borderless Data Table */
        .qf-result-header {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin-bottom: 1rem;
            flex-wrap: wrap;
            gap: 0.75rem;
        }
        .qf-result-title {
            font-family: 'Newsreader', Georgia, serif;
            font-size: 1.6rem;
            font-weight: 500;
            color: var(--ink-primary);
            margin: 0;
        }
        .qf-result-stats {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--ink-secondary);
        }
        .qf-table-scroll {
            width: 100%;
            overflow-x: auto;
            background: var(--bg-surface);
            border: 1px solid var(--rule-hairline);
            border-radius: 12px;
        }
        table.qf-editorial-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }
        table.qf-editorial-table th {
            padding: 0.85rem 1.1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--ink-muted);
            border-bottom: 1px solid var(--rule-hairline);
            background: #FAF9F6;
            white-space: nowrap;
        }
        table.qf-editorial-table td {
            padding: 0.85rem 1.1rem;
            border-bottom: 1px solid var(--rule-hairline);
            color: var(--ink-primary);
            white-space: nowrap;
        }
        table.qf-editorial-table tbody tr:last-child td {
            border-bottom: none;
        }
        table.qf-editorial-table tbody tr:hover {
            background-color: #FAF9F6;
        }

        /* Research Benchmark Hero Numbers (Typography-Driven) */
        .qf-bench-compare {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            gap: 2rem;
            padding: 2rem 0;
            border-top: 1px solid var(--rule-hairline);
            border-bottom: 1px solid var(--rule-hairline);
            margin: 1.5rem 0 2.5rem 0;
        }
        .qf-bench-stat {
            text-align: left;
        }
        .qf-bench-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--ink-muted);
        }
        .qf-bench-figure {
            font-family: 'Newsreader', Georgia, serif;
            font-size: clamp(3rem, 5.5vw, 4.5rem);
            font-weight: 500;
            line-height: 1.05;
            letter-spacing: -0.03em;
            margin: 0.35rem 0;
        }
        .qf-bench-caption {
            font-size: 0.88rem;
            color: var(--ink-secondary);
        }

        /* Clean Progressive Disclosure Expanders */
        details {
            background-color: transparent !important;
            border: none !important;
            border-bottom: 1px solid var(--rule-hairline) !important;
            border-radius: 0 !important;
            padding: 0.25rem 0 !important;
        }
        details summary {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            color: var(--ink-primary) !important;
            padding: 0.65rem 0 !important;
        }
        details summary:hover {
            color: var(--accent-cobalt) !important;
        }

        /* Mobile & Tablet Responsiveness */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
        }
        @media (max-width: 768px) {
            .block-container {
                padding-left: 1.15rem !important;
                padding-right: 1.15rem !important;
            }
            div[role="radiogroup"] {
                margin: 0 0 1.75rem 0 !important;
                justify-content: flex-start !important;
                gap: 1.1rem !important;
            }
            .qf-correction-rail {
                grid-template-columns: 1fr;
                gap: 0.9rem;
            }
            .qf-bench-compare {
                grid-template-columns: 1fr;
                gap: 1.25rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
