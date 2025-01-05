import React, { useEffect, useState } from "react";
import "./LoginRegister.css";
import Button from "../../components/button/Button";
import TextInput from "../../components/textInput/TextInput";
import Popup from "../../components/popup/Popup";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function LoginRegister({ handleAuth }) {
  const [login, setLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("étudiant");
  const [university, setUniversity] = useState("");
  const [speciality, setSpeciality] = useState("");
  const [qrCode, setQrCode] = useState("");
  const [popupMessage, setPopupMessage] = useState("");
  const [popupType, setPopupType] = useState(""); // success, error, warning
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/");
    }
  }, [navigate]);

  const handleClosePopup = () => {
    setPopupMessage("");
    setPopupType("");
  };

  const handleRegister = async () => {
    try {
      if (!email || !username || !password || !role) {
        setPopupMessage("Veuillez remplir tous les champs requis.");
        setPopupType("error");
        return;
      }

      const payload = { email, username, password, role };

      if (role === "étudiant") {
        if (!university || !speciality) {
          setPopupMessage(
            "L'université et la spécialité sont requises pour les étudiants."
          );
          setPopupType("error");
          return;
        }
        payload.university = university;
        payload.speciality = speciality;
      }

      const response = await axios.post("http://localhost:8000/register/", payload);

      setPopupMessage("Inscription réussie !");
      setPopupType("success");
      setLogin(true);
    } catch (error) {
      const errorMessage =
        error.response?.data?.message || "Échec de l'inscription. Veuillez réessayer.";
      setPopupMessage(errorMessage);
      setPopupType("error");
    }
  };

  const handleLogin = async () => {
    try {
      if (!email && !qrCode) {
        setPopupMessage(
          "Veuillez fournir un email et un mot de passe ou un QR code."
        );
        setPopupType("error");
        return;
      }

      const payload = qrCode ? { qr_code: qrCode } : { email, password };

      const response = await axios.post(
        "http://localhost:8000/login/",
        payload
      );

      const { token } = response.data;
      localStorage.setItem("token", token);
      // Redirection en fonction du rôle
   
      handleAuth();
      navigate("/");
    } catch (error) {
      const errorMessage =
        error.response?.data?.error || "Échec de la connexion. Veuillez réessayer.";
      setPopupMessage(errorMessage);
      setPopupType("error");
    }
  };

  return (
    <div className="login-screen">
      <div className="login-register-container">
        <div className="login-register-logo">IHEC</div>
        <div className="login-register-inputs">
          {login ? (
            <>
              <TextInput
                placeholder={"Email"}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                type={"email"}
              />
              <TextInput
                placeholder={"Mot de passe"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type={"password"}
              />
              <TextInput
                placeholder={"QR Code"}
                value={qrCode}
                onChange={(e) => setQrCode(e.target.value)}
                type={"text"}
              />
              <div onClick={() => setLogin(!login)} className="account-button">
                Pas de compte ?
              </div>
              <div className="row">
                <Button dark={false} text={"Annuler"} onClick={() => navigate(-1)} />
                <Button dark={true} text={"Connexion"} onClick={handleLogin} />
              </div>
            </>
          ) : (
            <>
              <TextInput
                placeholder={"Nom d'utilisateur"}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                type={"text"}
              />
              <TextInput
                placeholder={"Email"}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                type={"email"}
              />
              <TextInput
                placeholder={"Mot de passe"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type={"password"}
              />
              <label htmlFor="role">Choisissez un rôle :</label>
              <select
                id="role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="étudiant">Étudiant</option>
                <option value="bibliothécaire">Bibliothécaire</option>
                
              </select>
              {role === "étudiant" && (
                <>
                  <TextInput
                    placeholder={"Université"}
                    value={university}
                    onChange={(e) => setUniversity(e.target.value)}
                    type={"text"}
                  />
                  <TextInput
                    placeholder={"Spécialité"}
                    value={speciality}
                    onChange={(e) => setSpeciality(e.target.value)}
                    type={"text"}
                  />
                </>
              )}
              <div onClick={() => setLogin(!login)} className="account-button">
                Déjà un compte ?
              </div>
              <div className="row">
                <Button dark={false} text={"Annuler"} onClick={() => navigate(-1)} />
                <Button dark={true} text={"Inscription"} onClick={handleRegister} />
              </div>
            </>
          )}
        </div>
      </div>
      <Popup message={popupMessage} type={popupType} onClose={handleClosePopup} />
    </div>
  );
}
