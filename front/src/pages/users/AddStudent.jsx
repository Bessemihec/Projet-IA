import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './AddStudent.css'; // Import the provided CSS file

const AddUser = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    university: '',
    speciality: '',
    role: 'étudiant', // Default role set to "étudiant"
  });
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Send a POST request to create a new user
      await axios.post(
        'http://localhost:8000/register/',
        {
          username: formData.username,
          email: formData.email,
          password: formData.password,
          university: formData.role !== 'bibliothécaire' ? formData.university : undefined, // Only send university for non-librarians
          speciality: formData.role !== 'bibliothécaire' ? formData.speciality : undefined, // Only send speciality for non-librarians
          role: formData.role, // Use the selected role (étudiant or bibliothécaire)
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`, // Include the JWT token
          },
        }
      );

      // Success handling
      setSuccessMessage('Utilisateur ajouté avec succès!');
      setFormData({
        username: '',
        email: '',
        password: '',
        university: '',
        speciality: '',
        role: 'étudiant', // Reset the role to "étudiant" after success
      });

      // Redirect after 2 seconds
      setTimeout(() => navigate('/userlist'), 2000);
    } catch (err) {
      // Error handling
      setError(
        err.response?.data?.message || "Une erreur s'est produite lors de l'ajout de l'utilisateur."
      );
    }
  };

  return (
    <div className="add-student-container">
      <h1>Ajouter un utilisateur</h1>
      {error && <p className="error-message">{error}</p>}
      {successMessage && <p className="success-message">{successMessage}</p>}

      <form className="add-student-form" onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          placeholder="Nom d'utilisateur"
          required
        />
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Email"
          required
        />
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Mot de passe"
          required
        />
        
        {/* Role selection dropdown */}
        <select
          name="role"
          value={formData.role}
          onChange={handleChange}
          required
        >
          <option value="étudiant">Étudiant</option>
          <option value="bibliothécaire">Bibliothécaire</option>
        </select>

        {/* Université and spécialité inputs only for students */}
        {formData.role !== 'bibliothécaire' && (
          <>
            <input
              type="text"
              name="university"
              value={formData.university}
              onChange={handleChange}
              placeholder="Université"
              required
            />
            <input
              type="text"
              name="speciality"
              value={formData.speciality}
              onChange={handleChange}
              placeholder="Spécialité"
              required
            />
          </>
        )}

        <button type="submit">Ajouter</button>
        <button type="button" onClick={() => navigate('/userlist')}>
          Annuler
        </button>
      </form>
    </div>
  );
};

export default AddUser;
