import datetime

import streamlit as st

# باید اولین دستور streamlit باشد
st.set_page_config(
    page_title="سامانه پاسخگوی آموزشی دانشگاه",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# تم رسمی (سرمه‌ای + طلایی)، راست‌چین و کاملاً رسپانسیو
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap');

    :root {
        --navy: #1F3A5F;
        --navy-dark: #152A47;
        --gold: #B8962E;
        --bg: #F5F7FA;
        --border: #D9DEE7;
        --text: #1F2937;
    }

    *, *::before, *::after { box-sizing: border-box; }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        width: 100%;
        max-width: 100%;
        min-width: 0;
        overflow-x: hidden;
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
    }

    .stApp { background: var(--bg); }
    p, li, label, input, textarea, button,
    [data-testid="stMarkdownContainer"] {
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
        text-align: right;
    }

    /* Main Container: Centered Layout */
    [data-testid="stMain"] { min-width: 0; width: 100%; }
    [data-testid="stMainBlockContainer"] {
        width: 100% !important;
        max-width: 900px !important;
        min-width: 0 !important;
        margin-inline: auto !important;
        padding: 1.5rem 1rem 7rem !important;
    }

    .uni-header {
        width: 100%;
        min-width: 0;
        background: linear-gradient(135deg, var(--navy-dark), var(--navy));
        border-bottom: 4px solid var(--gold);
        border-radius: 14px;
        padding: 1.35rem 1.5rem;
        margin: 0 0 1.25rem;
        color: #fff;
        overflow-wrap: anywhere;
    }
    .uni-header h1 {
        color: #fff !important;
        font-size: clamp(1.1rem, 2.5vw, 1.55rem);
        line-height: 1.7;
        margin: 0 0 .35rem;
    }
    .uni-header p {
        color: #D8E1EE !important;
        font-size: .92rem;
        line-height: 1.9;
        margin: 0;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        width: 100%;
        min-width: 0;
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin: 0 0 .85rem;
        color: var(--text) !important;
        overflow-wrap: anywhere;
    }
    [data-testid="stChatMessage"] * {
        color: var(--text) !important;
        min-width: 0;
        overflow-wrap: anywhere;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {
        line-height: 1.95;
    }

    /* RTL Support for App Base & Chat */
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stChatMessage"],
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {
        direction: rtl !important;
        text-align: right !important;
    }

    /* Sidebar RTL Fixes & Drawer Behavior */
    [data-testid="stSidebar"] {
        direction: rtl !important;
        right: 0 !important;
        left: auto !important;
        border-left: 0 !important;
        border-right: 3px solid var(--gold) !important;
        text-align: right !important;
        background: #fff !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        direction: rtl !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        direction: rtl !important;
        text-align: right !important;
        color: var(--text) !important;
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
    }

    /* Buttons Style */
    .stButton > button, .stDownloadButton > button {
        width: 100%;
        min-height: 44px;
        height: auto;
        white-space: normal;
        overflow-wrap: anywhere;
        line-height: 1.7;
        padding: .65rem .85rem;
        background: #fff;
        color: var(--navy) !important;
        border: 1px solid var(--navy);
        border-radius: 10px;
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: var(--navy);
        color: #fff !important;
        border-color: var(--navy);
    }
    .stButton > button p, .stDownloadButton > button p { color: inherit !important; }

    [data-testid="stAlert"] {
        background: #EAF0F8 !important;
        border: 1px solid var(--navy) !important;
        border-radius: 12px;
    }
    [data-testid="stAlert"] * { color: var(--navy) !important; }

    [data-testid="stExpander"] {
        background: #fff !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px;
    }
    [data-testid="stExpander"] * { overflow-wrap: anywhere; }

    /* Chat Input Fixes */
    [data-testid="stBottom"] {
        background: linear-gradient(transparent, var(--bg) 18%) !important;
    }
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        background: var(--bg) !important;
    }
    [data-testid="stChatInput"] {
        width: 100% !important;
        max-width: 900px !important;
        margin-inline: auto !important;
    }
    [data-testid="stChatInput"] > div {
        background: #fff !important;
        border: 1.5px solid var(--navy) !important;
        border-radius: 16px !important;
    }
    [data-testid="stChatInput"] textarea {
        background: #fff !important;
        color: var(--text) !important;
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
        font-size: 16px !important;
        line-height: 1.8 !important;
    }

    [data-testid="stMarkdownContainer"] table {
        display: block;
        max-width: 100%;
        overflow-x: auto;
    }
    [data-testid="stMarkdownContainer"] pre,
    [data-testid="stMarkdownContainer"] code {
        max-width: 100%;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }

    .disclaimer {
        color: #6B7280;
        font-size: .78rem;
        line-height: 1.9;
        text-align: center;
        border-top: 1px solid var(--border);
        padding-top: .8rem;
        margin-top: 1.5rem;
    }

    /* Mobile Responsive Optimizations */
    @media (max-width: 768px) {
        [data-testid="stMainBlockContainer"] {
            padding: .85rem .75rem 6.5rem !important;
        }
        [data-testid="stSidebar"] {
            width: min(85vw, 300px) !important;
            min-width: min(85vw, 300px) !important;
        }
        .stButton > button, .stDownloadButton > button {
            min-height: 46px;
            font-size: .88rem;
        }
    }

    @media (max-width: 600px) {
        [data-testid="stMainBlockContainer"] {
            padding: .65rem .5rem 6.25rem !important;
        }
        .uni-header {
            padding: 1rem .85rem;
            margin-bottom: .8rem;
            border-radius: 10px;
        }
        .uni-header h1 {
            font-size: 1.05rem;
        }
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: .5rem !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# بارگذاری یک‌بار مصرف RAG
# --------------------------------------------------
@st.cache_resource(show_spinner="در حال آماده‌سازی سامانه...")
def load_rag():
    import rag

    if rag.vectorstore._collection.count() == 0:
        documents = rag.read_pdf_file(rag.PDF_PATH)
        chunks = rag.split_documents(documents)
        rag.index_documents(chunks)

    return rag


try:
    rag = load_rag()
except Exception as e:
    st.error(f"خطا در راه‌اندازی سامانه: {e}")
    st.stop()


# --------------------------------------------------
# توابع کمکی
# --------------------------------------------------
TOP_K = 3

EXAMPLE_QUESTIONS = [
    "دروس نیمسال اول چیست؟",
    "دروس نیمسال دوم چیست؟",
    "نقش و توانایی فارغ التحصیلان چیست؟",
    "پیش نیاز درس ساختمان داده چیست؟"
]


def answer_question(query):
    retrieved = rag.retrieve_chunks(query, k=TOP_K)

    if not retrieved:
        return "اطلاعات مرتبطی پیدا نشد.", []

    context_parts = []
    for doc, distance in retrieved:
        context_parts.append(
            f"منبع: {doc.metadata.get('source', '?')}\n"
            f"صفحه PDF: {doc.metadata.get('page', '?')}\n"
            f"متن:\n{doc.page_content}"
        )

    context = "\n\n---\n\n".join(context_parts)
    answer = rag.llm(query, context)

    best_doc, _ = retrieved[0]
    sources = [
        {
            "source": best_doc.metadata.get("source", "?"),
            "page": best_doc.metadata.get("page", "?"),
            "section": best_doc.metadata.get("section"),
            "text": best_doc.page_content,
        }
    ]

    return answer, sources


def show_sources(sources):
    s = sources[0]
    with st.expander("📚 منبع پاسخ"):
        title = f"**{s['source']}** — صفحه {s['page']}"
        if s["section"]:
            title += f" — {s['section']}"
        st.markdown(title)
        st.text(s["text"])


def set_pending(question):
    st.session_state.pending = question


def clear_chat():
    st.session_state.messages = []


def export_chat():
    lines = ["گزارش گفتگو - سامانه پاسخگوی آموزشی", "=" * 40, ""]
    for m in st.session_state.messages:
        who = "دانشجو" if m["role"] == "user" else "سامانه"
        lines.append(f"{who}:\n{m['content']}\n")
    return "\n".join(lines)


# --------------------------------------------------
# وضعیت نشست
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# سایدبار
# --------------------------------------------------
with st.sidebar:
    st.header("🎓 درباره سامانه")
    st.write(
        "این سامانه به پرسش‌های شما درباره آیین‌نامه آموزشی و "
        "انتخاب واحد پاسخ می‌دهد."
    )

    st.subheader("📌 راهنما")
    st.markdown(
        "- سؤال را کامل و مشخص بنویسید.\n"
        "- منبع هر پاسخ زیر آن قابل مشاهده است.\n"
        "- برای موارد قطعی به دفتر آموزش مراجعه کنید."
    )

    st.subheader("💡 نمونه سؤال‌ها")
    for i, q in enumerate(EXAMPLE_QUESTIONS):
        st.button(q, key=f"side_ex_{i}", on_click=set_pending, args=(q,))

    st.divider()
    st.button("🗑️ گفتگوی جدید", on_click=clear_chat)

    if st.session_state.messages:
        st.download_button(
            "⬇️ دریافت متن گفتگو",
            data=export_chat(),
            file_name=f"chat_{datetime.date.today()}.txt",
            mime="text/plain",
        )

# --------------------------------------------------
# هدر
# --------------------------------------------------
st.markdown(
    """
    <div class="uni-header">
        <h1>🎓 سامانه پاسخگوی آموزشی دانشگاه</h1>
        <p>پاسخ به پرسش‌های درسی و انتخاب واحد بر اساس آیین‌نامه آموزشی</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# دریافت ورودی
# --------------------------------------------------
user_input = st.chat_input("سؤال خود را بنویسید...")
prompt = user_input or st.session_state.pop("pending", None)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

# --------------------------------------------------
# پیام خوشامدگویی
# --------------------------------------------------
if not st.session_state.messages:
    st.info("سلام! 👋 سؤال خود را بنویسید یا یکی از نمونه‌سؤال‌های زیر را انتخاب کنید.")
    cols = st.columns(2)
    for i, q in enumerate(EXAMPLE_QUESTIONS):
        with cols[i % 2]:
            st.button(q, key=f"main_ex_{i}", on_click=set_pending, args=(q,))

# --------------------------------------------------
# نمایش تاریخچه
# --------------------------------------------------
for msg in st.session_state.messages:
    avatar = "🧑‍🎓" if msg["role"] == "user" else "🎓"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("sources"):
            show_sources(msg["sources"])

# --------------------------------------------------
# تولید پاسخ برای پیام جدید
# --------------------------------------------------
if prompt:
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("در حال جست‌وجو در آیین‌نامه..."):
            try:
                answer, sources = answer_question(prompt)
            except Exception as e:
                answer, sources = f"خطا در دریافت پاسخ: {e}", []

        st.markdown(answer)
        if sources:
            show_sources(sources)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )

# --------------------------------------------------
# پانویس
# --------------------------------------------------
st.markdown(
    '<div class="disclaimer">پاسخ‌ها بر اساس آیین‌نامه بارگذاری‌شده تولید می‌شوند '
    "و جنبه راهنما دارند؛ برای تصمیم نهایی به دفتر آموزش دانشکده مراجعه کنید.</div>",
    unsafe_allow_html=True,
)