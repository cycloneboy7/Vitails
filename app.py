
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from collections import deque

from config.parameters import SimulationConfig
from physiology.engine import PhysiologicalEngine
from monitoring.alerts import check_alerts


st.set_page_config(
    page_title="VITALIS | Patient Monitor",
    page_icon="🫀",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0b1120;
        color: #ffffff;
    }

    div[data-testid="stMetric"] {
        background-color: #172338;
        border: 1px solid #263750;
        padding: 15px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #a9bad0;
    }

    h1, h2, h3 {
        color: #e5efff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🫀 VITALIS")
st.caption("RESEARCH EDITION | VIRTUAL PATIENT MONITORING SYSTEM")

if "engine" not in st.session_state:

    config = SimulationConfig()

    st.session_state.engine = PhysiologicalEngine(config)

    st.session_state.ecg = deque(maxlen=1000)
    st.session_state.ppg = deque(maxlen=1000)
    st.session_state.resp = deque(maxlen=1000)
    st.session_state.bp = deque(maxlen=1000)

    st.session_state.history = []
    st.session_state.running = True


st.sidebar.title("Patient Controls")

st.sidebar.text("Patient ID: VITALIS-001")

condition = st.sidebar.selectbox(
    "Patient Scenario",
    [
        "Normal",
        "Tachycardia",
        "Bradycardia",
        "Hypoxia",
        "Hypoventilation",
        "Fever",
        "Hypotension",
        "Hypertension"
    ]
)

st.sidebar.markdown("---")

if st.sidebar.button("Reset Simulation"):

    st.session_state.clear()

    st.rerun()

st.sidebar.markdown("### Simulation Status")

st.sidebar.success("Simulation Engine Ready")


@st.fragment(run_every="200ms")
def live_dashboard():

    engine = st.session_state.engine

    readings = []

    # Generate 50 samples at 250 Hz
    for _ in range(50):

        reading = engine.step()

        readings.append(reading)

    latest = readings[-1]

    # Update waveform buffers
    for r in readings:

        st.session_state.ecg.append(r["ecg"])
        st.session_state.ppg.append(r["ppg"])
        st.session_state.resp.append(r["respiration"])
        st.session_state.bp.append(r["arterial_pressure"])

    st.session_state.history.extend(readings)

    # Keep history manageable
    if len(st.session_state.history) > 15000:

        st.session_state.history = (
            st.session_state.history[-15000:]
        )

    # VITALS
    st.subheader("Patient Vitals")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Heart Rate",
        f"{latest['heart_rate']:.1f} BPM"
    )

    c2.metric(
        "SpO₂",
        f"{latest['spo2']:.1f}%"
    )

    c3.metric(
        "Respiratory Rate",
        f"{latest['respiratory_rate']:.1f}/min"
    )

    c4.metric(
        "Pulse",
        f"{latest['pulse']:.1f} BPM"
    )

    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "Arterial Pressure",
        f"{latest['arterial_pressure']:.1f} mmHg"
    )

    c6.metric(
        "Cardiac Output",
        f"{latest['cardiac_output']:.2f} L/min"
    )

    c7.metric(
        "Body Temperature",
        f"{latest['body_temperature']:.2f} °C"
    )

    c8.metric(
        "Room Temperature",
        f"{latest['room_temperature']:.1f} °C"
    )

    st.caption(
        f"Humidity: {latest['humidity']:.1f}% | "
        f"Simulation time: {latest['time']:.2f} seconds"
    )

    # ECG
    st.subheader("Electrocardiogram (ECG)")

    ecg_fig = go.Figure()

    ecg_fig.add_trace(
        go.Scatter(
            y=list(st.session_state.ecg),
            mode="lines",
            name="ECG",
            line=dict(color="#00e676", width=1.5)
        )
    )

    ecg_fig.update_layout(
        template="plotly_dark",
        height=260,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Sample",
        yaxis_title="Amplitude",
        showlegend=False
    )

    st.plotly_chart(
        ecg_fig,
        use_container_width=True
    )

    # PPG AND RESPIRATION
    left, right = st.columns(2)

    with left:

        st.subheader("PPG Waveform")

        ppg_fig = go.Figure()

        ppg_fig.add_trace(
            go.Scatter(
                y=list(st.session_state.ppg),
                mode="lines",
                line=dict(color="#ff4081", width=1.5)
            )
        )

        ppg_fig.update_layout(
            template="plotly_dark",
            height=250,
            showlegend=False
        )

        st.plotly_chart(
            ppg_fig,
            use_container_width=True
        )

    with right:

        st.subheader("Respiratory Waveform")

        resp_fig = go.Figure()

        resp_fig.add_trace(
            go.Scatter(
                y=list(st.session_state.resp),
                mode="lines",
                line=dict(color="#40c4ff", width=1.5)
            )
        )

        resp_fig.update_layout(
            template="plotly_dark",
            height=250,
            showlegend=False
        )

        st.plotly_chart(
            resp_fig,
            use_container_width=True
        )

    # ARTERIAL PRESSURE
    st.subheader("Arterial Pressure Waveform")

    bp_fig = go.Figure()

    bp_fig.add_trace(
        go.Scatter(
            y=list(st.session_state.bp),
            mode="lines",
            line=dict(color="#ffab40", width=1.5)
        )
    )

    bp_fig.update_layout(
        template="plotly_dark",
        height=250,
        showlegend=False
    )

    st.plotly_chart(
        bp_fig,
        use_container_width=True
    )

    # ALERTS
    st.subheader("Patient Monitoring Alerts")

    # Existing alert function expects HR, SpO2, RR and BP
    alert_readings = {
        "heart_rate": latest["heart_rate"],
        "spo2": latest["spo2"],
        "respiratory_rate": latest["respiratory_rate"],
        "systolic_bp": latest["arterial_pressure"],
    }

    alerts = check_alerts(alert_readings)

    if alerts:

        for alert in alerts:

            st.error(f"⚠️ {alert}")

    else:

        st.success("No configured threshold alerts.")

    # DATA EXPORT
    st.subheader("Research Data Export")

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.download_button(
        "Download Patient Data CSV",
        data=history_df.to_csv(index=False),
        file_name="vitalis_patient_data.csv",
        mime="text/csv"
    )


live_dashboard()