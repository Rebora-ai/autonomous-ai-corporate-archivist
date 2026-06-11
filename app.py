import streamlit as st
import ollama
from pypdf import PdfReader

# Настройка премиум-интерфейса Rebora Docs Enterprise
st.set_page_config(page_title="Rebora Docs Enterprise", page_icon="📂", layout="wide")

# Инициализируем общее хранилище текста в памяти сессии
if "extracted_text" not in st.session_state:
    st.session_state["extracted_text"] = ""
if "loaded_files" not in st.session_state:
    st.session_state["loaded_files"] = []

# Боковая панель для пакетной загрузки документов
with st.sidebar:
    st.title("📂 Rebora Docs")
    st.subheader("System Status: Online")
    st.markdown("---")
    
    # Модифицированная кнопка: теперь принимает НЕСКОЛЬКО файлов одновременно
    uploaded_files = st.file_uploader(
        "Upload Corporate PDF Documents:", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    # Если файлы изменены или загружены новые
    if uploaded_files:
        current_file_names = [f.name for f in uploaded_files]
        # Проверяем, обновился ли список файлов, чтобы не перепарсивать их по кругу
        if current_file_names != st.session_state["loaded_files"]:
            combined_text = ""
            for uploaded_file in uploaded_files:
                with st.spinner(f"Indexing {uploaded_file.name}..."):
                    reader = PdfReader(uploaded_file)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            combined_text += f"\n--- Document: {uploaded_file.name} ---\n" + text + "\n"
            
            st.session_state["extracted_text"] = combined_text
            st.session_state["loaded_files"] = current_file_names
            st.success(f"✓ {len(uploaded_files)} documents indexed into local knowledge base!")
            
    st.markdown("---")
    st.info("Data Processing: 100% Local. Multi-document secure analysis engine.")

# Главный экран
st.title("🤖 Corporate AI Archivist & Analyst")
st.caption("Autonomous multi-document knowledge retrieval engine for US/EU enterprises.")

st.markdown("---")

# Если в базе есть текст хотя бы из одного документа — активируем чат
if st.session_state["extracted_text"]:
    st.markdown(f"### 💬 Multi-Document Chat Activated ({len(st.session_state['loaded_files'])} files loaded)")
    
    user_query = st.text_input("Ask a question across all connected documents:")
    
    if st.button("Query AI Agent", type="primary"):
        if user_query:
            with st.spinner("Analyzing cross-document intelligence..."):
                system_prompt = (
                    f"You are a Corporate AI Archivist. Answer the user's question using ONLY the following "
                    f"extracted documents context: {st.session_state['extracted_text']}. State clearly from which "
                    f"document you took the information. If the answer cannot be found in the context, say "
                    f"'Information not found in the uploaded archive.' Be precise, professional, and factual."
                )
                
                try:
                    response = ollama.chat(model='llama3', messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_query}
                    ])
                    
                    st.markdown("### 🤖 Cross-Document Analysis Result:")
                    st.info(response['message']['content'])
                    
                except Exception as e:
                    st.error(f"Error connecting to local LLM: {e}. Ensure Ollama is running.")
        else:
            st.warning("Please enter a question first.")
else:
    st.warning("⬅️ Please upload corporate PDF documents in the sidebar to activate the multi-document AI Agent.")
    st.markdown("### Advanced RAG Architecture Features:")
    st.markdown("""
    1. **Batch Upload:** Upload 2, 5, or 20 PDFs at once (Contracts, Estimates, Bills).
    2. **Cross-Reference Engine:** The AI compares data across different files simultaneously.
    3. **Source:** The response tells you exactly which file the information came from.
    """)
