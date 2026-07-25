import os

import plotly.graph_objects as go
import requests
import streamlit as st

if os.getenv("RUNNING_IN_DOCKER") == "true":
    BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
else:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="HomePilot AI", page_icon="🏠", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #07111f 0%, #111c2f 100%);
        color: #f5f7fb;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(91,140,255,0.18), rgba(255,127,80,0.12));
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 18px;
        padding: 0.9rem 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.20);
    }
    .stProgress > div > div {
        background: linear-gradient(90deg, #5b8cff, #ff7f50);
    }
    .stAlert, .stSuccess, .stWarning, .stError {
        border-radius: 14px;
    }
    .css-1d391kg, .css-1y4p8pa {
        background: transparent;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(7,17,31,0.98), rgba(17,28,47,0.95));
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebarNavItems"] a {
        border-radius: 10px;
        margin: 0.2rem 0;
    }
    [data-testid="stSidebarNavItems"] a:hover {
        background: rgba(91,140,255,0.18);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## HomePilot AI")
    st.markdown("### Intelligent household finance")
    st.markdown("- 📊 Dashboard")
    st.markdown("- 🧠 Insights")
    st.markdown("- ⚙️ Automation")
    st.markdown("---")
    st.caption("Designed for clarity, control, and a premium customer experience.")

st.markdown(
    """
    <div style="background: linear-gradient(90deg, rgba(91,140,255,0.20), rgba(255,127,80,0.16)); padding: 1.4rem 1.6rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.12); margin-bottom: 1.2rem;">
        <h1 style="margin: 0 0 0.3rem 0; font-size: 2.2rem;">HomePilot AI</h1>
        <p style="margin: 0; font-size: 1rem; color: #dfe7ff;">A premium, intelligent way to understand household spending with clarity and confidence.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
    if health_response.ok:
        payload = health_response.json()
        st.success(f"Backend connected: {payload['service']}")
    else:
        st.warning("Backend responded with an error")
except Exception as exc:
    st.error(f"Unable to reach backend: {exc}")
    st.stop()

summary_response = requests.get(f"{BACKEND_URL}/api/expenses/dashboard", timeout=5)
if summary_response.ok:
    summary = summary_response.json()
    st.markdown("### Premium expense intelligence")
    st.caption("A refined overview designed to feel like a modern financial operating system.")

    with st.expander("Import transactions", expanded=True):
        st.write("Upload CSV or Excel files with columns like: date, description, amount, category")
        sample_csv = "date,description,amount,category\n2026-07-01,Grocery run,45.50,Groceries\n2026-07-02,Electricity bill,80.00,Utilities"
        st.download_button(
            label="Download sample CSV",
            data=sample_csv,
            file_name="sample_transactions.csv",
            mime="text/csv",
            use_container_width=True,
        )
        uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])
        if uploaded_file is not None:
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/octet-stream")}
                endpoint = "/api/expenses/import/csv" if uploaded_file.name.lower().endswith(".csv") else "/api/expenses/import/excel"
                response = requests.post(f"{BACKEND_URL}{endpoint}", files=files, timeout=20)
                if response.ok:
                    payload = response.json()
                    st.success(f"Imported {payload.get('imported_count', 0)} transactions successfully.")
                    st.caption("Your dashboard will refresh with the latest records.")
                    st.rerun()
                else:
                    st.error("Import failed. Please check the file format and contents.")
            except Exception as exc:
                st.error(f"Import request failed: {exc}")

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Transactions", summary.get("transaction_count", 0))
    with metric_col2:
        st.metric("Total spending", f"{summary.get('total_spending', 0):.2f}")
    with metric_col3:
        if summary.get("monthly_summary") and len(summary["monthly_summary"]) >= 2:
            current = summary["monthly_summary"][-1]["total"]
            previous = summary["monthly_summary"][-2]["total"]
            delta = current - previous
            percent_change = round((delta / previous) * 100, 1) if previous else 0.0
            st.metric("MoM change", f"{delta:+.2f}", f"{percent_change:+.1f}%")
        else:
            st.metric("MoM change", "—", "Not enough data")

    if summary.get("monthly_summary"):
        months = [entry["month"] for entry in summary["monthly_summary"]]
        totals = [entry["total"] for entry in summary["monthly_summary"]]

        st.markdown("#### Performance overview")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            bar_fig = go.Figure(
                data=[go.Bar(x=months, y=totals, marker_color="#5b8cff", name="Monthly spending")]
            )
            bar_fig.update_layout(
                title="Monthly spending",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Month",
                yaxis_title="Amount",
                margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(bar_fig, use_container_width=True, config={"displayModeBar": False})

        with chart_col2:
            trend_fig = go.Figure()
            trend_fig.add_trace(
                go.Scatter(
                    x=months,
                    y=totals,
                    mode="lines+markers",
                    name="Spending trend",
                    line=dict(color="#ff7f50", width=3),
                    marker=dict(size=8),
                )
            )
            trend_fig.update_layout(
                title="Spending trend",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Month",
                yaxis_title="Amount",
                margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(trend_fig, use_container_width=True, config={"displayModeBar": False})

        insight_col1, insight_col2 = st.columns([1.3, 0.7])
        with insight_col1:
            if summary.get("category_breakdown"):
                category_breakdown = sorted(summary["category_breakdown"], key=lambda item: item["total"], reverse=True)
                categories = [entry["category"] for entry in category_breakdown]
                category_totals = [entry["total"] for entry in category_breakdown]
                category_fig = go.Figure(data=[go.Pie(labels=categories, values=category_totals, hole=0.4, marker_colors=["#5b8cff", "#ff7f50", "#43b581", "#f5c542", "#9b7bff"])])
                category_fig.update_layout(
                    title="Category breakdown",
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                st.plotly_chart(category_fig, use_container_width=True, config={"displayModeBar": False})

        with insight_col2:
            st.markdown("#### Top spending categories")
            total_category_value = sum(item["total"] for item in category_breakdown) or 1 if summary.get("category_breakdown") else 1
            if summary.get("category_breakdown"):
                for item in category_breakdown[:5]:
                    share = round((item["total"] / total_category_value) * 100, 1)
                    st.markdown(f"**{item['category']}** — {item['total']:.2f} ({share:.1f}%)")
                    st.progress(min(1.0, item["total"] / total_category_value))

        with st.expander("Set a budget"):
            with st.form("budget_form"):
                category = st.text_input("Category", placeholder="Groceries")
                monthly_limit = st.number_input("Monthly limit", min_value=0.0, step=10.0)
                month = st.text_input("Month", value="2026-07", placeholder="YYYY-MM")
                submitted = st.form_submit_button("Save budget")

                if submitted:
                    if not category.strip():
                        st.warning("Please enter a category name.")
                    else:
                        try:
                            response = requests.post(
                                f"{BACKEND_URL}/api/expenses/budget",
                                params={"category": category.strip(), "limit": float(monthly_limit), "month": month.strip() or None},
                                timeout=5,
                            )
                            if response.ok:
                                st.success("Budget saved successfully.")
                                st.session_state["budget_refresh"] = True
                                st.rerun()
                            else:
                                st.error("Unable to save budget right now.")
                        except Exception as exc:
                            st.error(f"Budget request failed: {exc}")

        if summary.get("budget_status"):
            st.markdown("#### Budget status")
            for item in summary["budget_status"]:
                status_text = "On track" if not item["is_over"] else "Over budget"
                st.markdown(f"**{item['category']}** · limit {item['limit']:.2f} · spent {item['spent']:.2f} · remaining {item['remaining']:.2f}")
                st.progress(min(1.0, item["spent"] / item["limit"]))
                st.caption(status_text)

        insight_row = st.columns(2)
        with insight_row[0]:
            if summary.get("monthly_change"):
                st.markdown("#### Monthly change")
                for item in summary["monthly_change"]:
                    delta_text = f"{item['change']:+.2f}" if item.get("change") else "0.00"
                    pct_text = f" ({item['percent_change']:+.1f}%)" if item.get("percent_change") is not None else ""
                    st.write(f"- {item['month']}: {item['total']:.2f} | change {delta_text}{pct_text}")

        with insight_row[1]:
            if summary.get("duplicate_candidates"):
                st.markdown("#### Possible duplicates")
                for item in summary["duplicate_candidates"]:
                    st.write(f"- {item['description']} · {item['amount']:.2f} · {item['date']} · {item['count']} entries")

        if summary.get("insights"):
            st.markdown("#### AI-style guidance")
            for item in summary["insights"]:
                icon = "💡" if item["type"] == "general" else "⚠️" if item["type"] == "budget" else "🔎"
                st.markdown(
                    f"<div style='padding: 0.85rem 1rem; border-radius: 14px; margin-bottom: 0.6rem; background: rgba(91,140,255,0.12); border: 1px solid rgba(255,255,255,0.12);'>"
                    f"<strong>{icon} {item.get('title', 'Insight')}</strong><br>{item['message']}</div>",
                    unsafe_allow_html=True,
                )

        with st.expander("View monthly breakdown"):
            for entry in summary["monthly_summary"]:
                st.write(f"- {entry['month']}: {entry['total']:.2f}")
else:
    st.info("No expense data yet. Import a CSV or Excel file through the API to begin.")
