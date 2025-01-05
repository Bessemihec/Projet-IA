import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './CreateReservation.css';

const CreateReservation = () => {
  const [bookId, setBookId] = useState('');
  const [studentId, setStudentId] = useState('');
  const [duration, setDuration] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate(); // Initialise useNavigate

  const handleReservation = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('token'); // Assumed JWT token is stored in localStorage

    if (!token) {
      setError('Token requis');
      return;
    }

    const reservationData = {
      book_id: bookId,
      student_id: studentId,
      duration: duration
    };

    try {
      const response = await axios.post('http://localhost:8000/reservation/create/', reservationData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.status === 201) {
        setMessage('Réservation créée avec succès');
        setBookId('');
        setStudentId('');
        setDuration('');
        setError('');
        // Redirection après 2 secondes
        setTimeout(() => {
          navigate('/reservations');
        }, 2000); // 2 secondes
      }
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.error || 'Erreur serveur');
      } else {
        setError('Une erreur s\'est produite');
      }
      setMessage('');
    }
  };

  return (
    <div className="reservation-container">
      <h2>Créer une réservation</h2>
      {message && <p className="success-message">{message}</p>}
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleReservation}>
        <div className="input-group">
          <label htmlFor="book-id">ID du Livre</label>
          <input
            type="text"
            id="book-id"
            value={bookId}
            onChange={(e) => setBookId(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="student-id">ID de l'Étudiant</label>
          <input
            type="text"
            id="student-id"
            value={studentId}
            onChange={(e) => setStudentId(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="duration">Durée de la réservation</label>
          <input
            type="text"
            id="duration"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="submit-btn">Réserver</button>
      </form>
    </div>
  );
};

export default CreateReservation;
