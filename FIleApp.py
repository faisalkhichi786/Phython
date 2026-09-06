import streamlit as st
from pathlib import Path
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="File Ops Console",
    page_icon="🗂",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');

    :root {
        --bg: #EEF1F5;
        --panel: #FFFFFF;
        --panel-alt: #F4F6F9;
        --border: #D6DCE3;
        --text: #1F2933;
        --text-dim: #5B6672;
        --teal: #1E8F82;
        --teal-hover: #17756A;
        --amber: #C97A1A;
        --red: #C6433B;
        --red-hover: #A83730;
    }

    html, body, [class*="css"], [data-testid="stAppViewContainer"],
    [data-testid="stMarkdownContainer"], p, span, div, label {
        font-family: 'Inter', sans-serif;
        color: var(--text) !important;
    }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
    [data-testid="stMain"], [data-testid="stMainBlockContainer"],
    [data-testid="stBottomBlockContainer"] {
        background-color: var(--bg) !important;
    }

    [data-testid="stHeader"] { background-color: transparent !important; }

    /* Force dark surfaces on every generic Streamlit container so no
       light-theme default can show through, without needing a
       separate .streamlit/config.toml theme file. */
    div[data-testid="stVerticalBlock"],
    div[data-testid="stHorizontalBlock"],
    div[data-testid="column"] {
        background-color: transparent !important;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background-color: var(--panel);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    .brand {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text) !important;
        padding: 1.1rem 0 0.2rem 0;
        letter-spacing: 0.2px;
    }

    .brand-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: var(--text-dim) !important;
        padding-bottom: 1.2rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1rem;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-dim) !important;
        padding: 0.4rem 0;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        color: var(--teal) !important;
    }

    /* Selected radio dot color */
    section[data-testid="stSidebar"] div[role="radiogroup"] label div:first-child {
        border-color: var(--teal) !important;
    }

    /* ---------- Path breadcrumb ---------- */
    .path-bar {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: var(--text-dim);
        background-color: var(--panel-alt);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 0.5rem 0.9rem;
        margin-bottom: 1.4rem;
    }
    .path-bar span { color: var(--teal); }

    /* ---------- Panels ---------- */
    .panel {
        background-color: var(--panel);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 2px rgba(31, 41, 51, 0.06);
    }

    .panel h3 {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1rem;
        font-weight: 500;
        margin-top: 0;
        margin-bottom: 1rem;
        color: var(--text);
    }

    /* ---------- Inputs (white typed text, dark field for contrast) ---------- */
    .stTextInput input, .stTextArea textarea {
        background-color: #2B333B !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 1px var(--teal) !important;
    }

    /* ---------- Labels (widget titles above inputs) ---------- */
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    .stRadio label p,
    .stCheckbox label p {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-dim) !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
    }

    /* Radio / checkbox option text in the main panel (not sidebar) */
    div[data-testid="stRadio"] label,
    div[data-testid="stCheckbox"] label {
        color: var(--text) !important;
        font-weight: 600 !important;
    }

    /* Placeholder text visibility */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #98A2AD !important;
        opacity: 1;
    }

    /* Code / preview blocks */
    [data-testid="stCodeBlock"] pre, [data-testid="stCodeBlock"] code {
        background-color: #F4F6F9 !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* ---------- Buttons ---------- */
    .stButton button {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        background-color: var(--teal);
        color: #FFFFFF !important;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1.1rem;
        transition: background-color 0.15s ease;
    }
    .stButton button:hover {
        background-color: var(--teal-hover);
        color: #FFFFFF !important;
    }

    .danger-zone .stButton button {
        background-color: var(--red);
        color: #FFFFFF !important;
    }
    .danger-zone .stButton button:hover {
        background-color: var(--red-hover);
    }

    /* ---------- Console log ---------- */
    .console {
        background-color: var(--panel-alt);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 0.9rem 1.1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        max-height: 260px;
        overflow-y: auto;
    }

    .console-line {
        padding: 0.25rem 0;
        border-left: 3px solid var(--border);
        padding-left: 0.7rem;
        margin-bottom: 0.3rem;
        color: var(--text-dim);
    }
    .console-line.ok { border-left-color: var(--teal); color: var(--text); }
    .console-line.err { border-left-color: var(--red); color: var(--text); }
    .console-line.info { border-left-color: var(--amber); color: var(--text); }

    .console-time { color: var(--text-dim); margin-right: 0.6rem; }

    hr { border-color: var(--border); }

    /* hide default streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "active_path" not in st.session_state:
    st.session_state.active_path = None


def log(status: str, message: str):
    """status: ok | err | info"""
    st.session_state.history.insert(
        0,
        {
            "status": status,
            "message": message,
            "time": datetime.now().strftime("%H:%M:%S"),
        },
    )


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown('<div class="brand">FILE OPS CONSOLE</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="brand-sub">local file management</div>',
        unsafe_allow_html=True,
    )

    operation = st.radio(
        "Operation",
        ["> create", "> read", "> update", "> delete"],
        label_visibility="collapsed",
    )
    operation = operation.replace("> ", "")

# ============================================================
# HEADER
# ============================================================

st.markdown(
    f'<div class="path-bar">~/file-ops/<span>{operation}</span></div>',
    unsafe_allow_html=True,
)

col_main, col_console = st.columns([1.4, 1], gap="large")

# ============================================================
# CREATE
# ============================================================

with col_main:
    if operation == "create":
        st.markdown('<div class="panel"><h3>Create a file</h3>', unsafe_allow_html=True)
        filename = st.text_input("File name", placeholder="e.g. notes.txt", key="create_name")
        content = st.text_area("Content", placeholder="Type the content to write...", key="create_content", height=140)

        if st.button("Create file", key="create_btn"):
            name = filename.strip()
            if not name:
                log("err", "Create failed — file name cannot be empty.")
            else:
                path = Path(name)
                if path.exists():
                    log("err", f"Create failed — '{name}' already exists.")
                else:
                    try:
                        with path.open("w", encoding="utf-8") as f:
                            f.write(content)
                        log("ok", f"Created '{name}'.")
                    except PermissionError:
                        log("err", f"Create failed — no permission to create '{name}'.")
                    except OSError as e:
                        log("err", f"Create failed — {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # READ
    # ========================================================

    elif operation == "read":
        st.markdown('<div class="panel"><h3>Read a file</h3>', unsafe_allow_html=True)
        filename = st.text_input("File name", placeholder="e.g. notes.txt", key="read_name")

        if st.button("Read file", key="read_btn"):
            name = filename.strip()
            if not name:
                log("err", "Read failed — file name cannot be empty.")
            else:
                path = Path(name)
                if not path.exists():
                    log("err", f"Read failed — '{name}' does not exist.")
                elif not path.is_file():
                    log("err", f"Read failed — '{name}' is not a file.")
                else:
                    try:
                        text = path.read_text(encoding="utf-8")
                        st.session_state["last_read"] = (name, text)
                        log("ok", f"Read '{name}' ({len(text)} chars).")
                    except UnicodeDecodeError:
                        log("err", f"Read failed — '{name}' is not valid UTF-8 text.")
                    except PermissionError:
                        log("err", f"Read failed — no permission to read '{name}'.")
                    except OSError as e:
                        log("err", f"Read failed — {e}")

        if "last_read" in st.session_state:
            name, text = st.session_state["last_read"]
            st.markdown(f"**{name}**")
            st.code(text if text else "(empty file)", language=None)
        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # UPDATE
    # ========================================================

    elif operation == "update":
        st.markdown('<div class="panel"><h3>Update a file</h3>', unsafe_allow_html=True)
        filename = st.text_input("File name", placeholder="e.g. notes.txt", key="update_name")

        action = st.radio(
            "Action",
            ["Rename", "Append content", "Overwrite file"],
            horizontal=True,
            key="update_action",
        )

        path = Path(filename.strip()) if filename.strip() else None

        if action == "Rename":
            new_name = st.text_input("New file name", key="rename_target")
            if st.button("Rename", key="rename_btn"):
                if not path:
                    log("err", "Rename failed — file name cannot be empty.")
                elif not path.exists() or not path.is_file():
                    log("err", f"Rename failed — '{filename}' does not exist.")
                elif not new_name.strip():
                    log("err", "Rename failed — new file name cannot be empty.")
                else:
                    new_path = Path(new_name.strip())
                    if new_path.exists():
                        log("err", f"Rename failed — '{new_name}' already exists.")
                    else:
                        try:
                            path.rename(new_path)
                            log("ok", f"Renamed '{filename}' to '{new_name}'.")
                        except PermissionError:
                            log("err", "Rename failed — permission denied.")
                        except OSError as e:
                            log("err", f"Rename failed — {e}")

        elif action == "Append content":
            data = st.text_area("Content to append", key="append_content", height=120)
            if st.button("Append", key="append_btn"):
                if not path:
                    log("err", "Append failed — file name cannot be empty.")
                elif not path.exists() or not path.is_file():
                    log("err", f"Append failed — '{filename}' does not exist.")
                else:
                    try:
                        with path.open("a", encoding="utf-8") as f:
                            if path.stat().st_size > 0:
                                f.write("\n")
                            f.write(data)
                        log("ok", f"Appended content to '{filename}'.")
                    except PermissionError:
                        log("err", "Append failed — permission denied.")
                    except OSError as e:
                        log("err", f"Append failed — {e}")

        elif action == "Overwrite file":
            data = st.text_area("New content", key="overwrite_content", height=120)
            if st.button("Overwrite", key="overwrite_btn"):
                if not path:
                    log("err", "Overwrite failed — file name cannot be empty.")
                elif not path.exists() or not path.is_file():
                    log("err", f"Overwrite failed — '{filename}' does not exist.")
                else:
                    try:
                        with path.open("w", encoding="utf-8") as f:
                            f.write(data)
                        log("ok", f"Overwrote '{filename}'.")
                    except PermissionError:
                        log("err", "Overwrite failed — permission denied.")
                    except OSError as e:
                        log("err", f"Overwrite failed — {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # DELETE
    # ========================================================

    elif operation == "delete":
        st.markdown(
            '<div class="panel danger-zone"><h3>Delete a file</h3>',
            unsafe_allow_html=True,
        )
        filename = st.text_input("File name", placeholder="e.g. notes.txt", key="delete_name")
        confirm = st.checkbox("I understand this cannot be undone", key="delete_confirm")

        if st.button("Delete file", key="delete_btn"):
            name = filename.strip()
            if not name:
                log("err", "Delete failed — file name cannot be empty.")
            elif not confirm:
                log("info", "Delete cancelled — confirmation not checked.")
            else:
                path = Path(name)
                if not path.exists() or not path.is_file():
                    log("err", f"Delete failed — '{name}' does not exist.")
                else:
                    try:
                        path.unlink()
                        log("ok", f"Deleted '{name}'.")
                        if st.session_state.get("last_read", (None,))[0] == name:
                            del st.session_state["last_read"]
                    except PermissionError:
                        log("err", "Delete failed — permission denied.")
                    except OSError as e:
                        log("err", f"Delete failed — {e}")

        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# CONSOLE LOG
# ============================================================

with col_console:
    st.markdown('<div class="panel"><h3>Activity log</h3>', unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown(
            '<div class="console"><div class="console-line">No operations yet — actions you run will show up here.</div></div>',
            unsafe_allow_html=True,
        )
    else:
        lines = "".join(
            f'<div class="console-line {h["status"]}">'
            f'<span class="console-time">{h["time"]}</span>{h["message"]}</div>'
            for h in st.session_state.history[:30]
        )
        st.markdown(f'<div class="console">{lines}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)