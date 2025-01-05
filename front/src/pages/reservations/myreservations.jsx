import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './ReservationsTable.css';

const MyReservations = () => {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userIdFromToken, setUserIdFromToken] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [currentReservation, setCurrentReservation] = useState(null);
  const navigate = useNavigate();

  const decodeToken = (token) => {
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      return payload._id;
    } catch (error) {
      console.error("Erreur lors du décodage du token:", error);
      return null;
    }
  };

  const fetchReservations = async (userId) => {
    try {
      const response = await axios.get('http://localhost:8000/reservations/all', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      const filteredReservations = response.data.filter(reservation => reservation.student_id === userId);

      const updatedReservations = await Promise.all(filteredReservations.map(async (reservation) => {
        const bookTitle = await fetchBookDetails(reservation.book_id);

        const currentDate = new Date();
        const endDate = new Date(reservation.date_fin_reservation);
        if (endDate < currentDate && reservation.status !== 'terminé') {
          await updateReservationStatus(reservation.id, 'terminé');
          reservation.status = 'terminé';
        }

        return {
          ...reservation,
          book: bookTitle,
        };
      }));

      setReservations(updatedReservations);
    } catch (error) {
      setError('Erreur lors du chargement des réservations');
    } finally {
      setLoading(false);
    }
  };

  const fetchBookDetails = async (bookId) => {
    try {
      const response = await axios.get(`http://localhost:8000/${bookId}/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      return response.data.Titre;
    } catch (error) {
      console.error('Erreur lors de la récupération du livre', error);
      return 'Livre non trouvé';
    }
  };

  const updateReservationStatus = async (reservationId, status) => {
    try {
      await axios.put(`http://localhost:8000/reservation/${reservationId}/update/`, { status }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
    } catch (error) {
      console.error('Erreur lors de la mise à jour du statut de la réservation', error);
    }
  };

  const handleDelete = async (reservationId) => {
    if (window.confirm("Êtes-vous sûr de vouloir supprimer cette réservation ?")) {
      try {
        await axios.delete(`http://localhost:8000/reservation/${reservationId}/delete/`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        setReservations(reservations.filter(reservation => reservation.id !== reservationId));
      } catch (error) {
        setError('Erreur lors de la suppression de la réservation');
      }
    }
  };

  const handleEdit = (reservationId) => {
    const reservationToEdit = reservations.find(reservation => reservation.id === reservationId);

    if (!reservationToEdit) {
      console.error('Réservation non trouvée', reservationId);
      return;
    }

    setCurrentReservation({
      student: reservationToEdit.student,
      book: reservationToEdit.book,
      date_reservation: reservationToEdit.date_reservation,
      duration: reservationToEdit.duration,
      status: reservationToEdit.status,
      id: reservationToEdit.id
    });
    setEditMode(true);
  };

  const handleSaveEdit = async () => {
    if (!currentReservation) {
      setError("Aucune réservation à mettre à jour");
      return;
    }

    const updatedDuration = currentReservation.duration;
    const updatedStatus = currentReservation.status;

    if (!updatedDuration || !updatedDuration.match(/^\d+ (hours|days)$/)) {
      setError('Veuillez entrer une durée valide sous la forme "X hours" ou "X days".');
      return;
    }

    const updatedReservation = {
      duration: updatedDuration,
      status: updatedStatus,
    };

    try {
      await axios.put(`http://localhost:8000/reservation/${currentReservation.id}/update/`, updatedReservation, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      setReservations(reservations.map(reservation =>
        reservation.id === currentReservation.id ? { ...reservation, ...updatedReservation } : reservation
      ));
      setEditMode(false);
    } catch (error) {
      setError("Erreur lors de la mise à jour de la réservation");
    }
  };

  const handleCancelEdit = () => {
    setEditMode(false);
    setCurrentReservation(null);
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const userId = decodeToken(token);
      setUserIdFromToken(userId);

      if (userId) {
        fetchReservations(userId);
      }
    } else {
      setLoading(false);
    }
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    return date.toLocaleDateString('fr-FR', options) + ' ' + date.toLocaleTimeString('fr-FR');
  };

  if (loading) return <p>Chargement...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="reservations-table-container">
      <h1>Liste des réservations</h1>

      {editMode ? (
        <div className="edit-form">
          <h2>Modifier la réservation</h2>
          <input
            type="text"
            value={currentReservation.duration}
            onChange={(e) => setCurrentReservation({ ...currentReservation, duration: e.target.value })}
            placeholder="Durée de la réservation"
          />
          <input
            type="text"
            value={currentReservation.status}
            onChange={(e) => setCurrentReservation({ ...currentReservation, status: e.target.value })}
            placeholder="Statut de la réservation"
          />
          <button className="save-btn" onClick={handleSaveEdit}>Sauvegarder</button>
          <button className="cancel-btn" onClick={handleCancelEdit}>Annuler</button>
        </div>
      ) : (
        <table className="reservations-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Titre du livre</th>
              <th>Date de réservation</th>
              <th>Durée</th>
              <th>Statut</th>
              <th>Date fin</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {reservations.map((reservation) => (
              <tr key={reservation.id}>
                <td>{reservation.id}</td>
                <td>{reservation.book}</td>
                <td>{formatDate(reservation.date_reservation)}</td>
                <td>{reservation.duration}</td>
                <td>{reservation.status}</td>
                <td>{formatDate(reservation.date_fin_reservation)}</td>
                <td>
                  <button className="edit-btn" onClick={() => handleEdit(reservation.id)}>Modifier</button>
                  <button className="delete-btn" onClick={() => handleDelete(reservation.id)}>Supprimer</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default MyReservations;
