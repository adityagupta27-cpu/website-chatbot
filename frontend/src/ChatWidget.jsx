import { useState, useEffect, useRef } from "react";
import API from "./api";

function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);

  const [message, setMessage] = useState("");

  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "👋 Hello! Ask me anything about E2M Solutions.",
    },
  ]);

  const chatBodyRef = useRef(null);

  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;

    // Add user's message immediately
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userMessage,
      },
    ]);

    setMessage("");

    setLoading(true);

    try {
      const response = await API.post("/chat", {
        question: userMessage,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: response.data.answer,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "❌ Something went wrong while contacting the server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        className="chat-button"
        onClick={() => setIsOpen(!isOpen)}
      >
        💬
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window">

          <div className="chat-header">
            <h3>E2M AI Assistant</h3>

            <button
              className="close-btn"
              onClick={() => setIsOpen(false)}
            >
              ✕
            </button>
          </div>

          <div
            className="chat-body"
            ref={chatBodyRef}
          >
            {messages.map((msg, index) => (
              <div
                key={index}
                className={
                  msg.sender === "user"
                    ? "user-message"
                    : "bot-message"
                }
              >
                {msg.text}
              </div>
            ))}

            {loading && (
              <div className="bot-message">
                Thinking...
              </div>
            )}
          </div>

          <div className="chat-input">
            <input
              type="text"
              placeholder="Type your question..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
            />

            <button
              onClick={sendMessage}
              disabled={loading}
            >
              Send
            </button>
          </div>

        </div>
      )}
    </>
  );
}

export default ChatWidget;