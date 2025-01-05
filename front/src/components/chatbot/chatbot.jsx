import React, { useState } from "react";

const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Bonjour, je suis un assistant de bibliothèque digital. Comment puis-je vous aider ?",
    },
  ]);
  const [userInput, setUserInput] = useState("");
  
  const sendMessage = async () => {
  if (userInput.trim() === "") return;

  const userMessage = { sender: "user", text: userInput };
  setMessages((prev) => [...prev, userMessage]);

  try {
    // Récupérer le token CSRF à partir des cookies ou des métadonnées
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const response = await fetch("http://localhost:8000/chatbot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken, // Ajouter le token CSRF ici
      },
      body: JSON.stringify({ query: userInput }),
    });

    const data = await response.json();
    const botMessage = { sender: "bot", text: data.response };
    setMessages((prev) => [...prev, botMessage]);
  } catch (error) {
    setMessages((prev) => [
      ...prev,
      { sender: "bot", text: "Erreur : Impossible de contacter le serveur." },
    ]);
  }

  setUserInput("");
};


  return (
    <div style={styles.chatbotContainer}>
      <div style={styles.chatWindow}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              alignSelf: msg.sender === "bot" ? "flex-start" : "flex-end",
              backgroundColor: msg.sender === "bot" ? "#f1f1f1" : "#007bff",
              color: msg.sender === "bot" ? "#000" : "#fff",
            }}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div style={styles.inputContainer}>
        <input
          type="text"
          style={styles.input}
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Tapez votre message..."
        />
        <button style={styles.button} onClick={sendMessage}>
          Envoyer
        </button>
      </div>
    </div>
  );
};

const styles = {
  chatbotContainer: {
    width: "400px",
    margin: "0 auto",
    border: "1px solid #ddd",
    borderRadius: "8px",
    overflow: "hidden",
    display: "flex",
    flexDirection: "column",
    fontFamily: "Arial, sans-serif",
  },
  chatWindow: {
    flex: 1,
    padding: "10px",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    overflowY: "auto",
    height: "300px",
    backgroundColor: "#f9f9f9",
  },
  message: {
    maxWidth: "70%",
    padding: "10px",
    borderRadius: "15px",
    fontSize: "14px",
  },
  inputContainer: {
    display: "flex",
    borderTop: "1px solid #ddd",
  },
  input: {
    flex: 1,
    padding: "10px",
    border: "none",
    outline: "none",
  },
  button: {
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    padding: "10px",
    cursor: "pointer",
  },
};

export default Chatbot;
