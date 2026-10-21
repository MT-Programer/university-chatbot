import datetime

import streamlit as st

# باید اولین دستور streamlit باشد
st.set_page_config(
    page_title="سامانه پاسخگوی آموزشی دانشگاه",
    page_icon="🎓",
    layout="centered",
)

# --------------------------------------------------
# تم رسمی (سرمه‌ای + طلایی) و راست‌چین
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700&display=swap');

    :root {
        --navy: #1F3A5F;
        --navy-dark: #152A47;
        --gold: #B8962E;
        --bg: #F5F7FA;
        --border: #D9DEE7;
    }

    html, body, .stApp, .stMarkdown, .stChatMessage, textarea, button {
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    .stApp { background-color: var(--bg); }

    /* هدر رسمی */
    .uni-header {
        background: linear-gradient(135deg, var(--navy-dark), var(--navy));
        border-bottom: 4px solid var(--gold);
        border-radius: 10px;
        padding: 22px 26px;
        margin-bottom: 18px;
        color: #fff;
    }
    .uni-header h1 {
        color: #fff; font-size: 1.5rem; margin: 0 0 6px 0; padding: 0;
    }
    .uni-header p { color: #D8E1EE; margin: 0; font-size: 0.9rem; }

    /* حباب پیام‌ها */
    [data-testid="stChatMessage"] {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }

    /* سایدبار */
    [data-testid="stSidebar"] {
        background-color: #fff;
        border-left: 3px solid var(--gold);
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--navy) !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
        color: #1F2937 !important;
    }
    /* متن داخل دکمه‌های سایدبار */
    [data-testid="stSidebar"] .stButton > button p,
    [data-testid="stSidebar"] .stDownloadButton > button p {
        color: inherit !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover,
    [data-testid="stSidebar"] .stDownloadButton > button:hover {
        color: #fff !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover p,
    [data-testid="stSidebar"] .stDownloadButton > button:hover p {
        color: #fff !important;
    }
    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] .stDownloadButton > button {
        color: var(--navy) !important;
    }

    /* دکمه‌ها */
    .stButton > button, .stDownloadButton > button {
        background: #fff;
        color: var(--navy);
        border: 1px solid var(--navy);
        border-radius: 8px;
        width: 100%;
        transition: all 0.15s;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: var(--navy);
        color: #fff;
        border-color: var(--navy);
    }

    /* ---- رنگ‌های اجباری صفحه اصلی (مستقل از تم تیره/روشن) ---- */
    [data-testid="stChatMessage"],
    [data-testid="stChatMessage"] * {
        color: #1F2937 !important;
    }

    [data-testid="stExpander"] {
        background: #fff !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary *,
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] *,
    [data-testid="stExpander"] pre,
    [data-testid="stExpander"] pre * {
        color: #1F2937 !important;
        background: transparent !important;
    }

    [data-testid="stAlert"] {
        background: #EAF0F8 !important;
        border: 1px solid var(--navy) !important;
    }
    [data-testid="stAlert"] * { color: var(--navy) !important; }

    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        background: var(--bg) !important;
    }
    [data-testid="stChatInput"] textarea {
        background: #fff !important;
        color: #1F2937 !important;
    }
    [data-testid="stChatInput"] > div {
        background: #fff !important;
        border: 1px solid var(--navy) !important;
    }

    .stButton > button p,
    .stDownloadButton > button p {
        color: inherit !important;
    }
    .stButton > button,
    .stDownloadButton > button {
        color: var(--navy) !important;
    }
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stButton > button:hover p,
    .stDownloadButton > button:hover p {
        color: #fff !important;
    }

    .disclaimer {
        font-size: 0.78rem; color: #6B7280; text-align: center;
        border-top: 1px solid var(--border);
        padding-top: 10px; margin-top: 24px;
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
    import rag  # ماژول چت‌بات شما

    # فقط اگر دیتابیس خالی بود، PDF ایندکس می‌شود
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
TOP_K = 3  # تعداد chunk ارسالی به مدل (ثابت و مخفی از کاربر)

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

    # فقط مرتبط‌ترین chunk به عنوان منبع نمایش داده می‌شود
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
# دریافت ورودی (از کادر چت یا دکمه نمونه‌سؤال)
# --------------------------------------------------
user_input = st.chat_input("سؤال خود را بنویسید...")
prompt = user_input or st.session_state.pop("pending", None)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

# --------------------------------------------------
# پیام خوشامدگویی (فقط وقتی گفتگو خالی است)
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
