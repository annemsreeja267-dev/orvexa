import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"


def check_backend_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=20)
        if response.status_code == 200:
            payload = response.json()
            return {
                "ok": True,
                "index_ready": payload.get("index_ready", False)
            }
        return {
            "ok": False,
            "index_ready": False
        }
    except requests.exceptions.RequestException:
        return {
            "ok": False,
            "index_ready": False
        }

def login(username, password):
    return requests.post(
        f"{API_BASE_URL}/login",
        json={
            "username": username,
            "password": password
        },
        timeout=60
    )


def ask_question(username, password, question):
    return requests.post(
        f"{API_BASE_URL}/query",
        json={
            "username": username,
            "password": password,
            "question": question
        },
        timeout=300
    )


def init_session():
    defaults = {
        "logged_in": False,
        "user": None,
        "username": "",
        "password": "",
        "last_answer": None,
        "last_sources": [],
        "question_input": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.username = ""
    st.session_state.password = ""
    st.session_state.last_answer = None
    st.session_state.last_sources = []
    st.session_state.question_input = ""


def render_sidebar():
    st.sidebar.title("Access Overview")
    st.sidebar.markdown(
        """
**Admin**
- All domains
- Public, internal, confidential

**Employee**
- Public documents
- Internal documents from assigned domain
- No confidential access

**Client**
- Public documents only
"""
    )

    st.sidebar.divider()
    st.sidebar.caption("Demo Accounts")
    st.sidebar.code(
        "admin1 / admin123\n"
        "gov_emp_1 / gov123\n"
        "hr_emp_1 / hr123\n"
        "client1 / client123"
    )

    st.sidebar.divider()
    health = check_backend_health()
    if health["ok"]:
        if health["index_ready"]:
            st.sidebar.success("Backend connected and index ready")
        else:
            st.sidebar.warning("Backend connected, index warming up")
    else:
        st.sidebar.error("Backend unavailable")

def render_login():
    st.markdown(
        """
<style>
.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    color: #e5e7eb;
}
.hero-card {
    padding: 1.4rem 1.2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827 0%, #172033 55%, #1f2937 100%);
    border: 1px solid #334155;
    margin-bottom: 1rem;
    color: #e5e7eb;
}
.info-card {
    padding: 1rem;
    border-radius: 16px;
    background: #111827;
    border: 1px solid #334155;
    color: #e5e7eb;
}
.answer-card {
    padding: 1rem;
    border-radius: 16px;
    background: #111827;
    border: 1px solid #334155;
    min-height: 180px;
    color: #e5e7eb;
    line-height: 1.6;
}
.source-card {
    padding: 0.8rem;
    border-radius: 14px;
    background: #111827;
    border: 1px solid #334155;
    margin-bottom: 0.6rem;
    font-size: 0.95rem;
    color: #e5e7eb;
}
.user-banner {
    padding: 1rem 1.1rem;
    border-radius: 16px;
    border: 1px solid #334155;
    margin-bottom: 1rem;
    color: #e5e7eb;
}
.app-subtitle {
    margin: 0.35rem 0 0;
    color: #cbd5e1;
    font-size: 1rem;
}
.section-label {
    color: #cbd5e1;
    font-weight: 600;
    margin-bottom: 0.35rem;
}
</style>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="hero-card">
  <h1 style="margin-bottom:0.3rem; color:#f8fafc;">Enterprise Knowledge Assistant</h1>
  <p class="app-subtitle">Secure role-aware enterprise document assistant</p>
  <p style="margin:0.45rem 0 0; color:#cbd5e1;">
    Query organizational knowledge with authenticated access, grounded answers, and clear source citations.
  </p>
</div>
""",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("Login")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        login_clicked = st.button("Login", use_container_width=True)

        if login_clicked:
            if not username or not password:
                st.error("Enter both username and password.")
                return

            try:
                response = login(username, password)
                if response.status_code == 200:
                    payload = response.json()
                    st.session_state.logged_in = True
                    st.session_state.user = payload["user"]
                    st.session_state.username = username
                    st.session_state.password = password
                    st.success("Login successful.")
                    st.rerun()
                else:
                    try:
                        detail = response.json().get("detail", "Login failed.")
                    except Exception:
                        detail = "Login failed."
                    st.error(detail)
            except requests.exceptions.RequestException as exc:
                st.error(f"Could not connect to backend: {exc}")

    with col2:
        st.markdown(
            """
<div class="info-card">
  <h3 style="margin-top:0; color:#f8fafc;">How Access Works</h3>
  <p style="color:#cbd5e1;"><strong>Admin:</strong> full access across all domains and classifications.</p>
  <p style="color:#cbd5e1;"><strong>Employee:</strong> public docs plus internal docs from their own domain.</p>
  <p style="color:#cbd5e1;"><strong>Client:</strong> public docs only.</p>
</div>
""",
            unsafe_allow_html=True
        )


def render_user_banner(user):
    role = user["role"]
    domain = user.get("domain") or "All domains"

    role_color = {
        "admin": "#fdba74",
        "employee": "#93c5fd",
        "client": "#86efac"
    }.get(role, "#e5e7eb")

    bg_color = {
        "admin": "#2b1a10",
        "employee": "#14243d",
        "client": "#0f2418"
    }.get(role, "#111827")

    st.markdown(
        f"""
<div class="user-banner" style="background: {bg_color};">
  <div style="display:flex; justify-content:space-between; align-items:center; gap:1rem;">
    <div>
      <div style="font-size:1.1rem; font-weight:700; color:#f8fafc;">Welcome, {user['username']}</div>
      <div style="color:#cbd5e1;">Role: <strong style="color:{role_color};">{role}</strong> | Domain: <strong style="color:#f8fafc;">{domain}</strong></div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True
    )


def render_app():
    user = st.session_state.user

    st.title("Enterprise Knowledge Assistant")
    st.caption("Secure role-aware enterprise document assistant")

    render_user_banner(user)

    top_left, top_right = st.columns([4, 1])
    with top_left:
        st.info("Tip: The first query after startup may take longer because the backend warms up the index.")
    with top_right:
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

    question = st.text_area(
        "Ask a question",
        key="question_input",
        height=140,
        placeholder="Example: What is the code of ethics?"
    )

    ask_clicked = st.button("Get Answer", type="primary", use_container_width=True)

    if ask_clicked:
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            try:
                with st.spinner("Retrieving answer from authorized documents..."):
                    response = ask_question(
                        st.session_state.username,
                        st.session_state.password,
                        question
                    )

                if response.status_code == 200:
                    payload = response.json()
                    st.session_state.last_answer = payload["answer"]
                    st.session_state.last_sources = payload.get("sources", [])
                else:
                    try:
                        detail = response.json().get("detail", "Query failed.")
                    except Exception:
                        detail = "Query failed."
                    st.error(detail)

            except requests.exceptions.RequestException as exc:
                st.error(f"Could not connect to backend: {exc}")

    if st.session_state.last_answer:
        answer_col, source_col = st.columns([1.8, 1])

        with answer_col:
            st.subheader("Answer")
            st.markdown(
                f"""
<div class="answer-card">
{st.session_state.last_answer}
</div>
""",
                unsafe_allow_html=True
            )

        with source_col:
            st.subheader("Sources")
            if st.session_state.last_sources:
                for idx, source in enumerate(st.session_state.last_sources, start=1):
                    st.markdown(
                        f"""
<div class="source-card">
<strong style="color:#f8fafc;">Source {idx}</strong><br>
<span style="color:#cbd5e1;">{source}</span>
</div>
""",
                        unsafe_allow_html=True
                    )
            else:
                st.info("No sources found.")


def main():
    st.set_page_config(
        page_title="Enterprise Knowledge Assistant",
        page_icon="📘",
        layout="wide"
    )
    init_session()
    render_sidebar()

    if not st.session_state.logged_in:
        render_login()
    else:
        render_app()


if __name__ == "__main__":
    main()
