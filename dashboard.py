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

st_autorefresh(interval=1000, key="dashboard_refresh")

METRICS_API = "http://127.0.0.1:8000/metrics"
EVENTS_API = "http://127.0.0.1:8000/events"
QUEUE_API = "http://127.0.0.1:8000/queue"
SEARCH_API = "http://127.0.0.1:8000/search"

st.title("🛡️ VigilanceAI")
st.subheader("Real-Time Multi-Modal Threat Stream Optimizer")

try:
    metrics = requests.get(METRICS_API, timeout=5).json()
    events = requests.get(EVENTS_API, timeout=5).json()
    queue = requests.get(QUEUE_API, timeout=5).json()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📊 Total Events", metrics["total_events"])
    c2.metric("🖥️ Local Decisions", metrics["local_only"])
    c3.metric("☁️ Cloud AI Calls", metrics["cloud_calls"])
    c4.metric("💰 Cost Savings", f'{metrics["savings_percent"]}%')

    q1, q2, q3 = st.columns(3)
    q1.metric("📦 Queue Size", queue["queue_size"])
    q2.metric("⚙️ Events Processed", queue["events_processed"])
    q3.metric("🟢 Active Workers", queue["active_workers"])

    st.progress(metrics["savings_percent"] / 100)
    st.success("Pipeline Status: Healthy")

    st.divider()

    if events:
        df = pd.DataFrame(events)

        st.subheader("🚨 Live Event Feed")
        latest = events[0]

        st.info(
            f"Latest Event: {latest['payload']} | "
            f"Risk: {latest['risk_level']} | "
            f"Route: {latest['route']}"
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

        st.subheader("🔍 Semantic Event Search")
        query = st.text_input("Search similar events", "suspicious package")

        if st.button("Search"):
            response = requests.get(
                SEARCH_API,
                params={"query": query, "limit": 5},
                timeout=10,
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

                    st.dataframe(
                        search_df,
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.info("No semantic matches found.")
            else:
                st.warning("Search endpoint returned no valid result.")

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
        st.info("No events yet.")

except Exception as e:
    st.error(e)