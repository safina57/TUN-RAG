import streamlit as st
import websocket
import time
import html  # To safely escape HTML in messages

# ------------------- CSS STYLING ------------------- #
st.markdown(
    """
    <style>
    /* Set overall page background and text color (optional) */
    .reportview-container .main {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    /* Hide default Streamlit header and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Chat container styling */
    .chat-container {
        max-width: 700px;
        margin: 0 auto;
        padding: 1rem;
    }
    /* Chat bubble common style */
    .chat-bubble {
        display: flex;
        align-items: flex-start;
        margin: 0.5rem 0;
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        line-height: 1.4;
    }
    .chat-bubble .icon {
        width: 32px;
        height: 32px;
        margin-right: 0.75rem;
        border-radius: 50%;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        color: #FFF;
    }
    /* User chat bubble styling */
    .user-bubble {
        background-color: #2F2F2F;
    }
    .user-bubble .icon {
        background-color: #FF6666;
    }
    /* Bot chat bubble styling */
    .bot-bubble {
        background-color: #3F3F3F;
    }
    .bot-bubble .icon {
        background-color: #FFC107;
    }
    .message-text {
        flex: 1;
        word-wrap: break-word;
        white-space: pre-wrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------- HELPER FUNCTIONS ------------------- #
def get_response(message: str) -> str:
    """Send a message via WebSocket to the FastAPI backend and return its response."""
    try:
        ws = websocket.create_connection("ws://localhost:8000/ws")
        ws.send(message)
        print("Message sent, waiting for response...")
        response = ws.recv()
        ws.close()
        return response
    except Exception as e:
        return f"Error: {e}"

def format_message(message: str) -> str:
    """
    Escape HTML and replace newlines with <br> so that paragraphs and line breaks are rendered properly.
    Wraps the content inside <p> tags.
    """
    escaped = html.escape(message)
    # Replace newline characters with <br> tags
    formatted = escaped.replace("\n", "<br>")
    return f"<p>{formatted}</p>"

def update_conversation_component():
    """Update the conversation component with the latest messages."""
    conversation_html = '<div class="chat-container">'
    for speaker, message in st.session_state.conversation:
        if speaker == "User":
            bubble_class = "user-bubble"
            icon = "👤"
        else:
            bubble_class = "bot-bubble"
            icon = "🤖"
        
        # Format the message content so that newlines are converted properly
        formatted_message = format_message(message)
        
        conversation_html += (
            f'<div class="chat-bubble {bubble_class}">'
            f'  <div class="icon">{icon}</div>'
            f'  <div class="message-text">{formatted_message}</div>'
            f'</div>'
        )
    conversation_html += "</div>"
    conversation_component.markdown(conversation_html, unsafe_allow_html=True)

def append_message(speaker: str, message: str):
    """Append a new message to the conversation state and update the component."""
    st.session_state.conversation.append((speaker, message))
    update_conversation_component()

# ------------------- SESSION STATE INITIALIZATION ------------------- #
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# ------------------- PAGE TITLE ------------------- #
st.title("Tunisian Constitution Chatbot")

# ------------------- CONVERSATION COMPONENT ------------------- #
# This container will be updated with the conversation history
conversation_component = st.empty()
update_conversation_component()

# ------------------- USER INPUT FORM ------------------- #
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Type your message here...",
        placeholder="Ask about the Tunisian constitution..."
    )
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    # Append user message and update the component immediately
    append_message("User", user_input)
    # Fetch bot response after a short delay so the user's message is visible
    time.sleep(0.1)
    bot_response = get_response(user_input)
    append_message("Bot", bot_response)
