import streamlit as st
import random

# ------------------ Page Config ------------------
st.set_page_config(page_title="Squares & Cubes Practice 🤖", page_icon="🤖", layout="centered")

# ------------------ Custom CSS for Glow Effect ------------------
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 36px !important;
            font-weight: bold;
            color: #3f2478;
            text-shadow: 0px 0px 10px #00f7ff, 0px 0px 20px #00f7ff;
        }
        .stChatMessage {
            border-radius: 12px !important;
            padding: 10px;
        }
        .sidebar-title {
            font-size: 22px !important;
            font-weight: bold;
            text-align: center;
            color: #3f2478;
            text-shadow: 0px 0px 5px #00f7ff;
        }
        .stButton button {
            background: linear-gradient(90deg, #00f7ff, #0077ff);
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 8px 16px;
            transition: 0.3s;
            border: none;
            box-shadow: 0px 0px 10px #00f7ff;
        }
        .stButton button:hover {
            background: linear-gradient(90deg, #0077ff, #00f7ff);
            box-shadow: 0px 0px 20px #00f7ff;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# ------------------ Title ------------------
st.markdown('<p class="main-title">Squares & Cubes Practice 🤖</p>', unsafe_allow_html=True)
st.write("✨ Let's practice! The computer gives you a number, you reply with its square or cube.")

# ------------------ Sidebar ------------------
with st.sidebar:
    st.markdown('<p class="sidebar-title">⚡ Practice Settings ⚡</p>', unsafe_allow_html=True)
    st.write("👉 Choose a mode in the chat to begin.")
    st.info("Type **square** or **cube** in the chat box to start.")
    st.write("---")
    st.markdown("🌟 **Quick Tips**")
    st.write("• Type 'exit' anytime to stop.\n• You get instant feedback.\n• Keep practicing to get better!")
    st.write("---")
    st.success("💡 Pro Tip: Challenge yourself by answering faster!")

# ------------------ Session State ------------------
if "mode" not in st.session_state:
    st.session_state.mode = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_number" not in st.session_state:
    st.session_state.current_number = None

# ------------------ Helper Function ------------------
def ask_number(mode):
    n = random.randint(1, 30 if mode == "square" else 25)
    st.session_state.current_number = n
    st.session_state.mode = mode
    st.session_state.messages.append({
        "role": "assistant",
        "content": f'What\'s the {"square" if mode == "square" else "cube"} of {n}? (Type "exit" to stop)'
    })

# ------------------ Display Messages ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ------------------ Chat Input Logic ------------------
if st.session_state.mode is None:
    choice = st.chat_input("Type 'square' or 'cube' to start practicing, or 'exit' to quit.")
    if choice:
        choice = choice.strip().lower()
        if choice in ["square", "cube"]:
            ask_number(choice)
        elif choice in ["exit", "stop", "quit"]:
            st.session_state.messages.append({"role": "assistant", "content": "🤖 Thanks for practicing! 🤖"})
            st.rerun()
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Please type 'square', 'cube', or 'exit'."})
        st.rerun()
else:
    prompt = st.chat_input(f"Type your answer for {st.session_state.mode}, or 'exit' to stop.")
    if prompt:
        txt = prompt.strip().lower()
        n = st.session_state.current_number
        if txt in ["exit", "stop", "quit"]:
            st.session_state.messages.append({"role": "assistant", "content": "Practice session ended. Type 'square' or 'cube' to start again, or 'exit' to quit."})
            st.session_state.mode = None
            st.rerun()
        else:
            try:
                user_answer = int(prompt)
                correct = n ** 2 if st.session_state.mode == "square" else n ** 3
                st.session_state.messages.append({"role": "user", "content": prompt})
                if user_answer == correct:
                    st.session_state.messages.append({"role": "assistant", "content": "✅ Well Done!!"})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": f"❌ Wrong! The correct answer is {correct}."})
                ask_number(st.session_state.mode)
            except ValueError:
                st.session_state.messages.append({"role": "assistant", "content": "Please enter a valid integer, or type 'exit' to stop."})
            st.rerun()
