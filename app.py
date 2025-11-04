import streamlit as st
from llama_cpp import Llama
import os

# -------------------------------
# Streamlit UI Configuration
# -------------------------------
st.set_page_config(page_title="🦙 Local Ollama Chatbot using GGUF", layout="wide")

st.title("🦙 Ollama Reasoning Chatbot (Local GGUF Model)")
st.markdown("Chat with your local Ollama model using llama.cpp")

# -------------------------------
# Sidebar Config
# -------------------------------
st.sidebar.header("⚙️ Model Settings")

model_path = st.sidebar.text_input(
    "Path to your local GGUF model file:",
    value=r"D:\PythonCertification\localslmchatbot\models\Llama-3.2-3B-Instruct-IQ3_M.gguf",
    help="Enter the full path to your downloaded GGUF file."
)

n_ctx = st.sidebar.slider("Context window (tokens)", 512, 8192, 2048, 256)
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.95, 0.05)
max_tokens = st.sidebar.slider("Max tokens to generate", 128, 4096, 512, 64)
n_threads = st.sidebar.slider("Threads", 1, 16, 4, 1)
n_gpu_layers = st.sidebar.slider("GPU layers (0 = CPU only)", 0, 32, 0, 1)

# -------------------------------
# Check model file
# -------------------------------
llm = None
if os.path.exists(model_path):
    file_size_gb = os.path.getsize(model_path) / (1024 ** 3)
    st.sidebar.info(f"Model file found: {file_size_gb:.2f} GB")
    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_gpu_layers=n_gpu_layers,
            verbose=False,
        )
        st.sidebar.success("✅ Model loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"❌ Failed to load model: {e}")
else:
    st.sidebar.warning("⚠️ Model file not found. Please check your path.")

# -------------------------------
# Chat Interface
# -------------------------------
st.markdown("### 💬 Chat Interface")

if llm:
    user_prompt = st.text_area("Enter your prompt here:", height=100)
    submit = st.button("Generate Response")

    if submit:
        if user_prompt.strip() == "":
            st.warning("Please enter a prompt to generate a response.")
        else:
            with st.spinner("Thinking..."):
                try:
                    response = llm(
                        user_prompt,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                    )
                    output = response["choices"][0]["text"]
                    st.markdown("#### 🧠 Model Response:")
                    st.write(output)
                except Exception as e:
                    st.error(f"❌ Failed to generate response: {e}")
else:
    st.info("Model not loaded yet. Please fix the issues in the sidebar before chatting.")
