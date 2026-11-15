import streamlit as st
import pandas as pd
import json

from agent import (
    analyze_experiment,
    analyze_experiment_json,
    compare_experiments_with_llm,
)
from experiment_memory import (
    initialize_database,
    save_experiment,
    get_experiments,
)

from log_parser import parse_training_log
from experiment_comparison import compare_experiments


# Page configuration
st.set_page_config(
    page_title="AI Experiment Debugger",
    page_icon="🔬",
    layout="wide",
)
initialize_database()

st.title("🔬 AI Experiment Debugger Agent")
st.caption("Powered by NVIDIA Nemotron on Nebius Token Factory")


# ----------------------------------
# 1. Upload and analyze training log
# ----------------------------------

st.header("1. Analyze Training Log")

uploaded_file = st.file_uploader(
    "Upload your ML training log",
    type=["log", "txt"],
    key="training_log",
)

if uploaded_file is not None:
    log_content = uploaded_file.getvalue().decode(
        "utf-8", errors="replace"
    )

    st.success("File uploaded successfully!")

    with st.expander("View Training Log"):
        st.text(log_content[:10000])

    df = parse_training_log(log_content)

    if not df.empty:
        st.subheader("Training Metrics")
        st.dataframe(df)

        st.subheader("Loss Curves")
        st.line_chart(
            df.set_index("epoch")[["train_loss", "val_loss"]]
        )

        st.subheader("Accuracy Curves")
        st.line_chart(
            df.set_index("epoch")[["train_acc", "val_acc"]]
        )
    else:
        st.warning("No supported epoch metrics found.")

    if st.button("Analyze Training Log"):
        with st.spinner("Analyzing with Nemotron..."):
            try:
                result = analyze_experiment_json(
                    log_content[:20000]
                )

                st.subheader("AI Diagnosis")
                st.json(result)

            except Exception as e:
                st.error(f"Analysis failed: {e}")


# ----------------------------------
# 2. Manual experiment analysis
# ----------------------------------

st.divider()
st.header("2. Analyze Experiment Manually")

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

    with st.spinner("Analyzing with Nemotron..."):
        try:
            result = analyze_experiment(experiment_data)

            st.subheader("AI Diagnosis")
            st.markdown(result)

        except Exception as e:
            st.error(f"Analysis failed: {e}")


# ----------------------------------
# 3. Compare two experiments
# ----------------------------------

st.divider()
st.header("3. Compare Two Experiments")

file_a = st.file_uploader(
    "Experiment A (Baseline)",
    type=["log", "txt"],
    key="compare_a",
)

file_b = st.file_uploader(
    "Experiment B (Modified)",
    type=["log", "txt"],
    key="compare_b",
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
        st.error("Could not parse both training logs.")

    else:
        comparison = compare_experiments(df_a, df_b)

    st.subheader("Save Experiment Comparison")

    experiment_name = st.text_input(
        "Experiment Name",
        value="Baseline vs Modified",
        key="comparison_name"
    )

    if st.button("Save Comparison"):
        try:
            experiment_id = save_experiment(
                experiment_name,
                comparison,
                {}
            )
            st.success(
                f"Comparison saved! Experiment ID: {experiment_id}"
            )
        except Exception as e:
            st.error(f"Could not save comparison: {e}")
        

        st.subheader("Metric Comparison")

        st.dataframe(
            pd.DataFrame({
                "Baseline": comparison["experiment_a"],
                "Modified": comparison["experiment_b"],
            })
        )

        change = comparison["improvement"]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Validation Accuracy Change",
                f'{change["val_accuracy_change"]:+.1f} pp',
            )

        with col2:
            st.metric(
                "Validation Loss Change",
                f'{change["val_loss_change"]:+.2f}',
            )

        if st.button("Analyze Comparison with Nemotron"):

            with st.spinner("Comparing experiments..."):
                try:
                    result = compare_experiments_with_llm(
                        comparison
                    )

                    st.subheader("AI Comparison")

                    st.write(result["summary"])

                    st.subheader("Improvements")
                    for item in result["improvements"]:
                        st.success(item)

                    st.subheader("Regressions")
                    for item in result["regressions"]:
                        st.warning(item)

                    st.subheader("Uncertainties")
                    for item in result["uncertainties"]:
                        st.info(item)

                    st.subheader("Recommended Next Experiment")
                    st.write(
                        result["next_experiment"]["description"]
                    )

                    st.write(
                        "**Evaluation Metric:**",
                        result["next_experiment"]["evaluation_metric"],
                    )

                    with st.expander("View JSON"):
                        st.json(result)

                except Exception as e:
                    st.error(f"Comparison failed: {e}")



st.divider()
st.header("4. Experiment History")

if st.button("Refresh History"):
    st.rerun()

experiments = get_experiments()

if experiments:
    history = pd.DataFrame(experiments)

    st.dataframe(
        history[["id", "created_at", "experiment_name"]],
        use_container_width=True
    )

    selected_id = st.selectbox(
        "View Saved Experiment",
        options=[exp["id"] for exp in experiments]
    )

    selected = next(
        exp for exp in experiments
        if exp["id"] == selected_id
    )

    st.subheader(selected["experiment_name"])
    st.json(json.loads(selected["metrics"]))

else:
    st.info("No saved experiments yet.")
