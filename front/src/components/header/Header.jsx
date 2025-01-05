import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import axios from "axios";
import "./Header.css";

const Header = ({ auth }) => {
  const [isAdmin, setIsAdmin] = useState(false); // Vérifie si l'utilisateur est admin
  const [isLibrarian, setIsLibrarian] = useState(false); // Vérifie si l'utilisateur est bibliothécaire
  const [isStudent, setIsStudent] = useState(false); // Vérifie si l'utilisateur est étudiant
  const [loading, setLoading] = useState(true); // Gère l'état de chargement
  const [error, setError] = useState(null); // Gère les erreurs lors de la récupération des données
  const location = useLocation();

  const isLoginPage =
    location.pathname === "/login-register" ||
    location.pathname === "/login-register/";

  const decodeToken = (token) => {
    try {
      const payload = JSON.parse(atob(token.split(".")[1])); // Décoder le payload du token
      return payload._id; // Retourner l'ID de l'utilisateur
    } catch (error) {
      console.error("Erreur lors du décodage du token:", error);
      return null;
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      const userId = decodeToken(token);
      if (userId) {
        fetchUserInfo(userId, token);
      }
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUserInfo = async (userId, token) => {
    try {
      const response = await axios.get(`http://localhost:8000/user/${userId}/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      // Vérifie les rôles
      setIsAdmin(response.data.role === "admin");
      setIsLibrarian(response.data.role === "bibliothécaire");
      setIsStudent(response.data.role === "étudiant"); // Vérification si l'utilisateur est étudiant
      setLoading(false);
    } catch (error) {
      console.error("Error fetching user info:", error);
      setError("Unable to fetch user info or user does not exist.");
      setLoading(false);
    }
  };

  if (isLoginPage || loading) {
    return null; // ou afficher un spinner de chargement ici
  }

  return (
    <div className="navigate-container">
      <div className="header-logo">IHEC</div>
      <Link to="/" className="navigate-button">
        Acceuil
      </Link>
      {isAdmin && (
        <>
          <Link to="/userlist" className="navigate-button">
            Liste des utilisateurs
          </Link>
          <Link to="/admin" className="navigate-button">
            Admin
          </Link>
          <Link to="/addbook" className="navigate-button">
            Ajouter livre
          </Link>
        </>
      )}

      {isLibrarian && (
        <Link to="/reservations" className="navigate-button">
          Reservations
        </Link>
      )}

      {isStudent && (
        <Link to="/myreservations" className="navigate-button">
          Mes réservations
        </Link>
      )}

      <Link
        to={auth ? "/profile" : "/login-register"}
        className="navigate-button profile-button"
      >
        {auth ? "Profile" : "Login"}
      </Link>
    </div>
  );
};

export default Header;
