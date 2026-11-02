
import streamlit as st
from agent import analyze_experiment

st.set_page_config(
    page_title="AI Experiment Debugger",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 AI Experiment Debugger Agent")
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
