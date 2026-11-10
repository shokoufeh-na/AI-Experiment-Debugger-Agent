
import streamlit as st
import json
from experiment_comparison import compare_experiments
from agent import analyze_experiment
from agent import analyze_experiment, analyze_experiment_json

import pandas as pd
from log_parser import parse_training_log
from agent import analyze_experiment_json




st.divider()
st.header("Compare Two Experiments")

file_a = st.file_uploader(
    "Upload Experiment A (Baseline)",
    type=["log", "txt"],
    key="experiment_a"
)

file_b = st.file_uploader(
    "Upload Experiment B (Modified)",
    type=["log", "txt"],
    key="experiment_b"
)

if file_a is not None and file_b is not None:
    log_a = file_a.getvalue().decode(
        "utf-8", errors="replace"
    )
    log_b = file_b.getvalue().decode(
        "utf-8", errors="replace"
    )

    df_a = parse_training_log(log_a)
    df_b = parse_training_log(log_b)

    if df_a.empty or df_b.empty:
        st.error("Could not extract metrics from both logs.")
    else:
        comparison = compare_experiments(df_a, df_b)

        st.subheader("Metric Comparison")
        st.dataframe(
            pd.DataFrame({
                "Baseline": comparison["experiment_a"],
                "Modified": comparison["experiment_b"]
            })
        )

        change = comparison["improvement"]

        st.metric(
            "Validation Accuracy Change",
            f'{change["val_accuracy_change"]:+.1f} pp'
        )

        st.metric(
            "Validation Loss Change",
            f'{change["val_loss_change"]:+.3f}'
        )

        if st.button("Analyze Comparison with Nemotron"):
            prompt = (
                "Compare these two ML experiments. "
                "Explain what improved, what worsened, "
                "and recommend the next experiment. "
                "Do not invent configurations or causes.\n\n"
                + json.dumps(comparison, indent=2)
            )

            with st.spinner("Comparing experiments..."):
                try:
                    result = analyze_experiment_json(prompt)
                    st.subheader("AI Comparison")
                    st.json(result)
                except Exception as e:
                    st.error(f"Comparison failed: {e}")









st.set_page_config(
    page_title="AI Experiment Debugger",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 AI Experiment Debugger Agent")
st.subheader("Upload Training Log")

uploaded_file = st.file_uploader(
    "Upload your ML training log",
    type=["log", "txt", "csv"]
)

if uploaded_file is not None:
    log_content = uploaded_file.getvalue().decode(
        "utf-8", errors="replace"
    )

    st.success("File uploaded successfully!")

    with st.expander("View Training Log"):
        st.text(log_content[:10000])

    if st.button("Analyze Training Log"):
        with st.spinner("Analyzing with NVIDIA Nemotron..."):
            try:
                # result = analyze_experiment(log_content[:20000])
                result = analyze_experiment_json(log_content[:20000])

                st.subheader("AI Diagnosis")
                # st.markdown(result)

                st.subheader("AI Diagnosis")
                st.error(result["diagnosis"])

                st.write("**Severity:**", result["severity"])

                st.subheader("Evidence")
                for item in result["evidence"]:
                    st.write("•", item)

                st.subheader("Likely Causes")
                for item in result["likely_causes"]:
                    st.write("•", item)

                st.subheader("Recommended Fixes")
                for item in result["recommended_fixes"]:
                    st.write("•", item)

                st.subheader("Next Experiment")
                st.info(result["next_experiment"])


            except Exception as e:
                st.error(f"Analysis failed: {e}")
st.write("Powered by NVIDIA Nemotron on Nebius Token Factory")

st.subheader("Experiment Information")

model = st.text_input("Model", "CNN")
dataset = st.text_input("Dataset", "CIFAR-10")

col1, col2 = st.columns(2)

with col1:
    train_accuracy = st.number_input(
        "Training Accuracy (%)", value=94.0
    )
    train_loss = st.number_input(
        "Training Loss", value=0.12
    )

with col2:
    val_accuracy = st.number_input(
        "Validation Accuracy (%)", value=61.0
    )
    val_loss = st.number_input(
        "Validation Loss", value=1.34
    )

if st.button("Analyze Experiment", type="primary"):

    experiment_data = f"""
    Model: {model}
    Dataset: {dataset}

    Training accuracy: {train_accuracy}%
    Validation accuracy: {val_accuracy}%

    Training loss: {train_loss}
    Validation loss: {val_loss}

    Diagnose this experiment.
    """

    with st.spinner("Analyzing with NVIDIA Nemotron..."):
        try:
            result = analyze_experiment(experiment_data)
            st.subheader("AI Diagnosis")
            st.markdown(result)
        except Exception as e:
            st.error(f"Analysis failed: {e}")



st.divider()
st.header("Compare Two Experiments")

file_a = st.file_uploader(
    "Experiment A (Baseline)",
    type=["log", "txt"],
    key="compare_a"
)

file_b = st.file_uploader(
    "Experiment B (Modified)",
    type=["log", "txt"],
    key="compare_b"
)

if file_a is not None and file_b is not None:
    log_a = file_a.getvalue().decode("utf-8", errors="replace")
    log_b = file_b.getvalue().decode("utf-8", errors="replace")

    df_a = parse_training_log(log_a)
    df_b = parse_training_log(log_b)

    if df_a.empty or df_b.empty:
        st.error("Could not parse both training logs.")
    else:
        comparison = compare_experiments(df_a, df_b)

        st.subheader("Metric Comparison")

        st.dataframe(pd.DataFrame({
            "Baseline": comparison["experiment_a"],
            "Modified": comparison["experiment_b"]
        }))

        change = comparison["improvement"]

        st.metric(
            "Validation Accuracy Change",
            f'{change["val_accuracy_change"]:+.1f} pp'
        )

        st.metric(
            "Validation Loss Change",
            f'{change["val_loss_change"]:+.2f}'
        )

        if st.button("Analyze Comparison with Nemotron"):
            prompt = (
                "Compare the following ML experiments. "
                "Explain improvements, regressions, and uncertainties. "
                "Recommend the next experiment. "
                "Do not invent missing configurations.\n\n"
                + json.dumps(comparison, indent=2)
            )

            with st.spinner("Analyzing comparison..."):
                try:
                    result = analyze_experiment_json(prompt)
                    st.subheader("AI Comparison")
                    st.json(result)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
