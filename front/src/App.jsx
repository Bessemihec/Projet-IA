import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginRegister from "./pages/loginRegister/LoginRegister";
import Profile from "./pages/profile/Profile";
import Bookshelf from "./pages/bookshelf/Bookshelf";
import Home from "./pages/home/Home";
import Header from "./components/header/Header";
import "./App.css";
import Book from "./pages/book/Book";
import UsersTable from "./pages/users/UsersTable";
import AddStudent from "./pages/users/AddStudent";
import Home_Admin from "./pages/home/Home_Admin";
import Book_Admin from "./pages/book/Book_Admin";
import AddBook from "./pages/book/AddBook";
import Chatbot from "./components/chatbot/chatbot";

function App() {
  const [auth, setAuth] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setAuth(true);
    } else {
      setAuth(false);
    }
  }, []);

  const handleAuth = () => {
    setAuth(!auth);
  };


  return (
    <Router>
      <div className="screen">
        <Header className="app-header" auth={auth} />
        <div className="routes">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route
              path="/login-register"
              element={<LoginRegister handleAuth={handleAuth} />}
            />
            <Route
              path="/profile"
              element={<Profile handleAuth={handleAuth} />}
            />
            <Route path="/bookshelf" element={<Bookshelf auth={auth} />} />

            <Route path="/:_id" element={<Book />} />

            <Route path="/create" element={<AddStudent />} />
            <Route
              path="/userlist"
              element={<UsersTable handleAuth={handleAuth} />}
            />
            <Route path="/Admin" element={<Home_Admin />} />
            <Route path="/Admin/:_id" element={<Book_Admin />} />
            <Route path="/AddBook" element={<AddBook />} />
            <Route path="/chatbot" element={<Chatbot/>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
