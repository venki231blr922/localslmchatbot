from llama_cpp import Llama

model_path = r"D:\PythonCertification\localslmchatbot\models\jamba-reasoning-3b-Q4_K_M.gguf"

llm = Llama(model_path=model_path, n_ctx=2048, n_gpu_layers=0)
print("✅ Model loaded successfully!")
