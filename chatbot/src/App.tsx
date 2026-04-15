import { useState } from "react";
import "./App.css";
import "./irisai-theme.css"

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages: Message[] = [
      ...messages,
      { role: "user", content: input }
    ];

    setMessages(newMessages);
    setInput("");

    const res = await fetch("http://127.0.0.1:8080/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        messages: newMessages
      })
    });

    const reader = res.body?.getReader();
    const decoder = new TextDecoder();

    let assistantText = "";

    setMessages([
      ...newMessages,
      { role: "assistant", content: "" }
    ]);

    if (!reader) return;

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });

      // SSE parsing básico
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const text = line.replace("data: ", "");

          assistantText += text;

          setMessages((prev) => {
            const copy = [...prev];
            copy[copy.length - 1] = {
              role: "assistant",
              content: assistantText
            };
            return copy;
          });
        }
      }
    }
  };

  return (
    <div className="container">
      {/* HEADER */}
      <div className="header">
        <h1 className="wp-block-heading irisai-h1">Ask anything about			<span className="irisai-grad">Your Site</span></h1>
      </div>

      <p className="irisai-sub">Get instant answers about services, pricing, support, and more.		</p>

      {/* CHAT */}
      <div className="chat">
        {messages.length === 0 && (
          <div className="empty">Escribe algo para empezar...</div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`message ${msg.role === "user" ? "user" : "bot"}`}
          >
            {msg.content}
          </div>
        ))}
      </div>

      {/* INPUT */}
      <div className="wp-block-group irisai-bar is-nowrap is-layout-flex">
        <input
          className="irisai-input"
          style={{ border: 'none', background: 'transparent', outline: 'none', flexGrow: 1 }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Escribe tu mensaje..."
        />
        <div className="wp-block-button irisai-btn">
          <a 
            className="wp-block-button__link wp-element-button"
            onClick={() => sendMessage()}
            style={{ cursor: 'pointer' }}
          >
            Enviar
          </a>
        </div>
      </div>
    </div>
  );
}