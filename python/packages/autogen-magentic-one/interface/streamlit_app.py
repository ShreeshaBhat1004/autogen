import streamlit as st
import asyncio
from magentic_one_helper import MagenticOneHelper
from datetime import datetime
import os

# Set page config
st.set_page_config(page_title="Magentic-One Interface", page_icon="🤖", layout="wide")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_chat_index' not in st.session_state:
    st.session_state.current_chat_index = None
if 'task_completed' not in st.session_state:
    st.session_state.task_completed = False
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Apply current theme
theme_class = 'dark-theme' if st.session_state.theme == 'dark' else 'light-theme'
st.markdown(f"""
    <style>
        body {{
            transition: all 0.5s ease;
        }}
    </style>
    <script>
        document.body.className = '{theme_class}';
    </script>
""", unsafe_allow_html=True)

# Load CSS
current_dir = os.path.dirname(os.path.abspath(__file__))
css_file = os.path.join(current_dir, "style.css")
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Task templates
TASK_TEMPLATES = {
    "Web Research": "Search and summarize information about [topic]",
    "Code Analysis": "Analyze the code in [repository/file] and provide insights",
    "Data Processing": "Process the data in [file] and generate a report",
    "System Command": "Execute and explain the results of [command]",
    "Custom Task": ""
}

def reset_chat():
    st.session_state.current_chat_index = None
    st.session_state.task_completed = False

def format_agent_message(source, message):
    """Format agent messages with consistent styling"""
    icons = {
        "Orchestrator": "🎯",
        "WebSurfer": "🌐",
        "FileSurfer": "📁",
        "Coder": "💻",
        "ComputerTerminal": "⌨️"
    }
    icon = icons.get(source.split()[0], "🤖")
    return f"""
    <div class="agent-message">
        <div style="font-weight: bold; margin-bottom: 0.5rem;">
            {icon} {source}
        </div>
        <div style="white-space: pre-wrap; line-height: 1.5;">
            {message}
        </div>
    </div>
    """

# Main layout
try:
    # Header section
    col1, col2 = st.columns([8, 1])
    with col1:
        st.markdown("<h1 style='margin: 0;'>🤖 Magentic-One Interface</h1>", unsafe_allow_html=True)
    with col2:
        icon = '🌞' if st.session_state.theme == 'dark' else '🌙'
        if st.button(icon, key='theme_toggle', help='Toggle Dark/Light Mode'):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.experimental_rerun()
    st.markdown("<hr>", unsafe_allow_html=True)

    # Columns layout
    left_col, main_col = st.columns([1.5, 4])

    # Left Panel
    with left_col:
        st.subheader("💬 Chat History")
        if st.button("➕ New Chat", key="new_chat"):
            reset_chat()

        search_query = st.text_input("Search...", key="search_chats")

        # Display chat history items
        for idx, chat in enumerate(st.session_state.chat_history):
            if search_query.lower() in chat['task'].lower():
                if st.button(f"🗨️ {chat['task']}", key=f"chat_{idx}"):
                    st.session_state.current_chat_index = idx
                    st.session_state.task_completed = True

    # Main Content
    with main_col:
        if st.session_state.current_chat_index is None:
            # Task input
            st.subheader("🚀 Start a New Task")
            template_type = st.selectbox("Choose a task template:", list(TASK_TEMPLATES.keys()), key="template_selector")
            task_placeholder = TASK_TEMPLATES[template_type]
            task = st.text_input("Describe your task:", value=task_placeholder if task_placeholder else "", key="task_input")
            if st.button("Run Task", key="run_task", disabled=not task.strip()):
                new_chat = {
                    'task': task,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'logs': [],
                    'final_answer': None
                }
                st.session_state.chat_history.append(new_chat)
                st.session_state.current_chat_index = len(st.session_state.chat_history) - 1
                st.session_state.task_completed = False
                st.experimental_rerun()
        else:
            # Display selected chat
            chat = st.session_state.chat_history[st.session_state.current_chat_index]
            st.subheader(f"📜 Task: {chat['task']}")
            st.write(f"🕒 {chat['timestamp']}")
            st.markdown("---")

            # Status containers
            status_container = st.empty()
            agent_container = st.container()
            result_container = st.empty()

            if not st.session_state.task_completed:
                async def run_magentic_one():
                    try:
                        status_container.info("Initializing Magentic-One...")
                        magnetic_one = MagenticOneHelper(logs_dir="./my_logs")
                        await magnetic_one.initialize()

                        task_future = asyncio.create_task(magnetic_one.run_task(chat['task']))

                        async for log_entry in magnetic_one.stream_logs():
                            st.session_state.chat_history[st.session_state.current_chat_index]['logs'].append(log_entry)
                            if "source" in log_entry and "message" in log_entry:
                                source = log_entry["source"]
                                message = log_entry["message"]

                                with agent_container:
                                    st.markdown(format_agent_message(source, message), unsafe_allow_html=True)

                        await task_future

                        final_answer = magnetic_one.get_final_answer()
                        if final_answer:
                            st.success(f"**Final Answer:**\n{final_answer}")
                            st.session_state.chat_history[st.session_state.current_chat_index]['final_answer'] = final_answer
                        else:
                            st.error("No final answer found.")

                        st.session_state.task_completed = True
                        status_container.empty()

                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                        status_container.empty()

                asyncio.run(run_magentic_one())
            else:
                # Display chat history
                for log_entry in chat['logs']:
                    if "source" in log_entry and "message" in log_entry:
                        source = log_entry["source"]
                        message = log_entry["message"]
                        st.markdown(format_agent_message(source, message), unsafe_allow_html=True)
                if chat['final_answer']:
                    st.success(f"**Final Answer:**\n{chat['final_answer']}")

            if st.button("🔄 Restart Task", key="restart_task"):
                reset_chat()
                st.experimental_rerun()

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")