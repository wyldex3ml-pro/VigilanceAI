import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="VigilanceAI Dashboard",
    page_icon="🛡️",
    layout="wide",
)

st_autorefresh(interval=3000, key="dashboard_refresh")

API_BASE_URL = "https://vigilanceai-vt78.onrender.com"

METRICS_API = f"{API_BASE_URL}/metrics"
EVENTS_API = f"{API_BASE_URL}/events"
QUEUE_API = f"{API_BASE_URL}/queue"
SEARCH_API = f"{API_BASE_URL}/search"

st.title("🛡️ VigilanceAI")
st.subheader("Real-Time Multi-Modal Threat Stream Optimizer")

try:
    metrics = requests.get(METRICS_API, timeout=15).json()
    events = requests.get(EVENTS_API, timeout=15).json()
    queue = requests.get(QUEUE_API, timeout=15).json()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📊 Total Events", metrics.get("total_events", 0))
    c2.metric("🖥️ Local Decisions", metrics.get("local_only", 0))
    c3.metric("☁️ Cloud AI Calls", metrics.get("cloud_calls", 0))
    c4.metric("💰 Cost Savings", f'{metrics.get("savings_percent", 0)}%')

    q1, q2, q3 = st.columns(3)
    q1.metric("📦 Queue Size", queue.get("queue_size", 0))
    q2.metric("⚙️ Events Processed", queue.get("events_processed", 0))
    q3.metric("🟢 Active Workers", queue.get("active_workers", 0))

    st.progress(metrics.get("savings_percent", 0) / 100)
    st.success("Backend Status: Connected")

    st.divider()

    if events:
        df = pd.DataFrame(events)

        st.subheader("🚨 Live Event Feed")
        latest = events[0]

        st.info(
            f"Latest Event: {latest.get('payload', 'N/A')} | "
            f"Risk: {latest.get('risk_level', 'N/A')} | "
            f"Route: {latest.get('route', 'N/A')}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Risk Score Timeline")
            df["event_number"] = range(len(df), 0, -1)
            chart = px.line(df, x="event_number", y="risk_score", markers=True)
            st.plotly_chart(chart, use_container_width=True, key="risk_timeline_chart")

        with col2:
            st.subheader("🥧 Risk Distribution")
            pie = px.pie(df, names="risk_level")
            st.plotly_chart(pie, use_container_width=True, key="risk_distribution_chart")

        st.subheader("☁️ Local vs Cloud Usage")
        bar = px.histogram(df, x="route")
        st.plotly_chart(bar, use_container_width=True, key="local_cloud_chart")

        st.divider()

        st.subheader("📋 Recent Events")
        st.dataframe(
            df[
                [
                    "timestamp",
                    "media_type",
                    "payload",
                    "risk_level",
                    "risk_score",
                    "route",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No cloud events yet. Backend is connected and running in lightweight deployment mode.")

    st.divider()

    st.subheader("🔍 Semantic Event Search")
    query = st.text_input("Search similar events", "suspicious package")

    if st.button("Search"):
        response = requests.get(
            SEARCH_API,
            params={"query": query, "limit": 5},
            timeout=15,
        )

        if response.status_code == 200:
            search_data = response.json()
            results = search_data.get("results", [])

            if results:
                search_df = pd.DataFrame(
                    [
                        {
                            "score": round(item["score"], 4),
                            "payload": item["event"]["payload"],
                            "risk_level": item["event"]["risk_level"],
                            "route": item["event"]["route"],
                        }
                        for item in results
                    ]
                )
                st.dataframe(search_df, use_container_width=True, hide_index=True)
            else:
                st.info(search_data.get("message", "Semantic search is in lightweight API mode."))
        else:
            st.warning("Search endpoint returned no valid result.")

except Exception as e:
    st.error(f"Could not connect to backend: {e}")