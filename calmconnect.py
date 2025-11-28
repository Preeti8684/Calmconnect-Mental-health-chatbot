import streamlit as st
from pymongo import MongoClient
import ollama
import time

st.set_page_config(page_title="CalmConnect", layout="wide")

# ----------------- GLOBAL THEME -----------------
st.markdown("""
<style>

/* Full page background gradient */
body, .main, .block-container, [data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, #f7d9ff, #e9c3ff, #d6a8ff) !important;
    color: #4a0072 !important;
}

/* Headings, paragraphs, divs, spans */
h1, h2, h3, p, div, span {
    color: #4a0072 !important;
    font-family: 'Poppins', sans-serif;
}

.centered { text-align: center; }

/* Cards */
.card {
    background: rgba(255, 255, 255, 0.65);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 4px 14px rgba(120, 0, 180, 0.15);
    text-align: center;
    backdrop-filter: blur(10px);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 20px rgba(120, 0, 180, 0.25);
}
.card-title {
    font-size: 22px;
    font-weight: 700;
    color: #4a0072;
}
.card-text {
    font-size: 16px;
    color: #4a0072;
}

/* Sidebar background and text */
[data-testid="stSidebar"] {
    background-color: white !important;
    color: black !important;
}

/* Button background and text */
.stButton>button {
    background-color: white !important;
    color: black !important;
    border: 1px solid #4a0072;
    border-radius: 8px;
    padding: 0.4em 1em;
}

/* Text input and chat input */
input, textarea {
    background-color: white !important;
    color: black !important;
    border: 1px solid #4a0072 !important;
    border-radius: 6px !important;
    padding: 4px 8px !important;
}

/* Remove Streamlit dark overlay */
.css-18e3th9 {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------- DATABASE -----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["calmconnect_db"]
users = db["users"]

# ----------------- SESSION -----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------- PAGE SWITCH -----------------
def go_to(page):
    st.session_state.page = page
    st.rerun()

# ----------------- HOME SCREEN -----------------
if st.session_state.page == "home":
    st.markdown("<div class='centered'><h1>Welcome to CalmConnect 🌿</h1></div>", unsafe_allow_html=True)
    st.markdown("<div class='centered'><h3>Your AI partner for emotional wellness.</h3></div>", unsafe_allow_html=True)

    st.write("")

    # --------- New Cards (4 Cards) ----------
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>💬 Emotional Support</div>
            <p class='card-text'>Talk about stress, anxiety, or anything on your mind.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>🧘 Mindful Guidance</div>
            <p class='card-text'>Personalized wellness and relaxation suggestions.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>🌈 Daily Uplift</div>
            <p class='card-text'>Daily motivation, mood boost & self-care reminders.</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>📘 Wellness Journal</div>
            <p class='card-text'>Track your emotions and build healthy habits.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # -------- Buttons ----------
    if st.button("💜 Get Started", use_container_width=True):
        go_to("login")

    st.write("")
    st.markdown("### New User?")
    if st.button("Signup", use_container_width=True):
        go_to("signup")

    st.write("")
    st.markdown("### Already Registered?")
    if st.button("Signin", use_container_width=True):
        go_to("login")

# ----------------- LOGIN PAGE -----------------
elif st.session_state.page == "login":
    from auth_pages.login import show_login
    show_login(go_to)

# ----------------- SIGNUP PAGE -----------------
elif st.session_state.page == "signup":
    from auth_pages.signup import show_signup
    show_signup(go_to)

# ----------------- MAIN APP AFTER LOGIN -----------------
elif st.session_state.page == "main_app":

    st.sidebar.title("🌿 CalmConnect")
    page = st.sidebar.radio(
        "Navigate",
        ["Home", "Meditation", "Chat", "Settings"]
    )

    st.sidebar.success(f"👋 Logged in as {st.session_state.user}")

    # ---------- HOME ----------
    if page == "Home":
        st.title("🏡 CalmConnect Home")
        st.write("Enjoy mindfulness tools, wellness chat, and meditation.")

    # ---------- MEDITATION ----------
    elif page == "Meditation":
        st.title("🧘 Meditation")
        st.write("Close your eyes and relax…")
        if st.button("Start 5s Breath"):
            for i in range(5):
                st.write("Inhale…")
                time.sleep(1)
                st.write("Exhale…")
                time.sleep(1)
            st.success("Done ✔")

    # ---------- CHAT ----------
    elif page == "Chat":
        st.title("💬 CalmConnect Chat")

        if not st.session_state.messages:
            st.session_state.messages.append(
                {"role": "assistant", "content": "Hello! How can I support you today?"}
            )

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt = st.chat_input("Type your message...")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = ollama.chat(
                            model="llama3",
                            messages=st.session_state.messages
                        )
                        reply = response["message"]["content"]
                    except:
                        reply = "Sorry, I am having trouble. Try again."

                    st.write(reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

    # ---------- SETTINGS ----------
    elif page == "Settings":
        st.title("⚙️ Settings")

        st.subheader("🎨 Theme Options (Coming Soon)")
        theme = st.selectbox("Choose Theme", ["Default Pink", "Light Mode", "Dark Mode"], index=0)

        st.write("")

        st.subheader("👤 Update Profile (Coming Soon)")
        st.text_input("Update username:")
        st.text_input("Update password:", type="password")
        st.button("Save Changes")

        st.write("")

        st.subheader("🗑️ Delete Profile (Coming Soon)")
        st.button("Delete My Account")

        st.write("")

        st.subheader("📜 Chat History (Coming Soon)")
        st.button("View Chat History")

        st.info("These features will be added in the next update. 💜")
