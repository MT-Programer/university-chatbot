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
# تم رسمی و بهینه‌شده برای موبایل (RTL واقعی)
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

    /* تنظیم فونت و جهت متن کلی */
    html, body, .stApp {
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
        direction: rtl;
        text-align: right;
        background-color: var(--bg);
    }

    /* اصلاح راست‌چین متن‌ها بدون دستکاری ساختار دکمه‌ها و آیکون‌ها */
    p, li, label, input, textarea, h1, h2, h3, h4,
    [data-testid="stMarkdownContainer"] {
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
        text-align: right !important;
        direction: rtl !important;
    }

    /* کانتینر اصلی صفحه */
    [data-testid="stMainBlockContainer"] {
        max-width: 800px !important;
        padding: 1rem 1rem 6rem 1rem !important;
        margin: 0 auto !important;
    }

    /* هدر سامانه */
    .uni-header {
        background: linear-gradient(135deg, var(--navy-dark), var(--navy));
        border-bottom: 4px solid var(--gold);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        color: #fff;
    }
    .uni-header h1 {
        color: #fff !important;
        font-size: 1.3rem;
        margin-bottom: .4rem;
    }
    .uni-header p {
        color: #D8E1EE !important;
        font-size: .88rem;
        margin: 0;
    }

    /* پیام‌های چت */
    [data-testid="stChatMessage"] {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: .8rem 1rem;
        margin-bottom: .75rem;
    }

    /* اصلاح سایدبار بدون خراب کردن آیکون‌ها */
    [data-testid="stSidebar"] {
        background-color: #fff !important;
        border-left: 2px solid var(--border);
    }

    /* تنظیم استایل دکمه‌ها */
    .stButton > button, .stDownloadButton > button {
        width: 100%;
        min-height: 42px;
        border-radius: 8px;
        background: #fff;
        color: var(--navy) !important;
        border: 1px solid var(--navy);
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
    }
    .stButton > button:hover {
        background: var(--navy);
        color: #fff !important;
    }
    .stButton > button p { color: inherit !important; }

    /* پانویس */
    .disclaimer {
        color: #6B7280;
        font-size: .75rem;
        text-align: center !important;
        border-top: 1px solid var(--border);
        padding-top: .8rem;
        margin-top: 1.5rem;
    }

    /* -------------------------------------------------- */
    /* تنظیمات مخصوص موبایل (Responsive Fixes) */
    /* -------------------------------------------------- */
    @media (max-width: 600px) {
        [data-testid="stMainBlockContainer"] {
            padding: .5rem .5rem 6.5rem .5rem !important;
        }

        .uni-header {
            padding: .9rem;
            border-radius: 10px;
        }

        .uni-header h1 {
            font-size: 1.05rem;
        }

        .uni-header p {
            font-size: .78rem;
        }

        /* تبدیل ستون‌های نمونه سوال به تک‌ستونی در موبایل */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: .4rem !important;
        }

        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
        }

        /* اصلاح عرض سایدبار بازشده در موبایل */
        [data-testid="stSidebar"] {
            width: 80vw !important;
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