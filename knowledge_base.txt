"""Streamlit entry point for the Local RAG Assistant."""

from __future__ import annotations

import streamlit as st

from src.config import DEFAULT_CHAT_MODEL, DEFAULT_EMBEDDING_MODEL, DATASET_PATH
from src.ollama_service import OllamaUnavailableError, check_ollama, stream_answer
from src.rag import build_index, retrieve


st.set_page_config(page_title="Local RAG Assistant", page_icon="📚", layout="wide")


@st.cache_resource(show_spinner=False)
def load_index(dataset_path: str, embedding_model: str):
    """Build the in-memory index once for each dataset/model combination."""
    return build_index(dataset_path, embedding_model)


def reset_chat() -> None:
    st.session_state.messages = []
    st.session_state.last_sources = []


if "messages" not in st.session_state:
    reset_chat()

with st.sidebar:
    st.title("📚 Local RAG Assistant")
    st.caption("Private, local question answering powered by Ollama.")
    st.divider()
    chat_model = st.text_input("Chat model", value=DEFAULT_CHAT_MODEL)
    embedding_model = st.text_input("Embedding model", value=DEFAULT_EMBEDDING_MODEL)
    top_k = st.slider("Context chunks", min_value=1, max_value=5, value=3)
    st.caption(f"Knowledge base: `{DATASET_PATH.name}`")
    if st.button("Clear conversation", use_container_width=True):
        reset_chat()
        st.rerun()

    available, detail = check_ollama()
    if available:
        st.success("Ollama is running")
    else:
        st.error("Ollama is not available")
        st.caption(detail)

st.title("Ask your local knowledge base")
st.write(
    "This app retrieves relevant notes from a local text file, then asks a local Ollama model "
    "to answer using only that context."
)

try:
    with st.spinner("Preparing the knowledge base…"):
        index = load_index(str(DATASET_PATH), embedding_model)
except OllamaUnavailableError as error:
    st.error(str(error))
    st.info("Start Ollama, pull the embedding model, then reload this page. See the README for commands.")
    st.stop()
except Exception as error:  # Keep startup failures understandable for new users.
    st.exception(error)
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Knowledge chunks", len(index.chunks))
col2.metric("Embedding model", embedding_model.split("/")[-1][:22])
col3.metric("Chat model", chat_model.split("/")[-1][:22])

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about the sample knowledge base…")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    try:
        sources = retrieve(question, index, top_k=top_k)
        st.session_state.last_sources = sources
        history = st.session_state.messages[:-1]
        with st.chat_message("assistant"):
            placeholder = st.empty()
            answer = ""
            for token in stream_answer(question, sources, history, chat_model):
                answer += token
                placeholder.markdown(answer + "▌")
            placeholder.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except OllamaUnavailableError as error:
        st.error(str(error))
    except Exception as error:
        st.error(f"Could not generate an answer: {error}")

if st.session_state.last_sources:
    with st.expander("Retrieved context", expanded=False):
        for result in st.session_state.last_sources:
            st.markdown(f"**Similarity: {result.score:.3f}**  ")
            st.write(result.chunk)
            st.divider()
