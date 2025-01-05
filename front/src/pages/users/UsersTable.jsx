import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Importation du hook useNavigate
import './UsersTable.css'; // Import des styles

const UsersTable = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const navigate = useNavigate(); // Déclaration de la variable navigate

  const handleEdit = (userId) => {
    // Trouver l'utilisateur à modifier
    const userToEdit = users.find(user => user._id === userId);
    setCurrentUser(userToEdit);
    setEditMode(true);  // Activer le mode édition
    console.log(`Modifier l'utilisateur avec l'ID: ${userId}`);
  };

  const handleDelete = async (userId) => {
    try {
      // Effectuer une requête DELETE pour supprimer l'utilisateur
      await axios.delete(`http://localhost:8000/users/${userId}/delete/`, { 
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,  // Ajoutez le token JWT si nécessaire
        }
      });
      // Mettre à jour la liste des utilisateurs après la suppression
      setUsers(users.filter(user => user._id !== userId)); // Mise à jour de l'état de la liste
      console.log(`Utilisateur avec l'ID: ${userId} supprimé`);
    } catch (error) {
      console.error('Erreur lors de la suppression de l\'utilisateur', error);
    }
  };

  const handleCancelEdit = () => {
    setEditMode(false);
    setCurrentUser(null);
  };

  const handleSaveEdit = async () => {
    try {
      // Effectuer une requête PUT pour mettre à jour l'utilisateur
      const updatedUser = {
        username: currentUser.username, // Ajoutez username à la mise à jour
        email: currentUser.email,
        role: currentUser.role, // Le rôle ne sera pas modifié
        // Inclure seulement les champs modifiables
        university: currentUser.role !== 'bibliothécaire' ? currentUser.university : undefined, // Ne pas inclure université et spécialité pour les bibliothécaires
        speciality: currentUser.role !== 'bibliothécaire' ? currentUser.speciality : undefined,
      };

      const response = await axios.put(`http://localhost:8000/users/${currentUser._id}/edit/`, updatedUser, { // Changé le chemin PUT
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        }
      });

      // Mettre à jour la liste des utilisateurs avec l'utilisateur modifié
      setUsers(users.map(user => 
        user._id === currentUser._id ? { ...user, ...updatedUser } : user // Mise à jour dans la liste
      ));

      setEditMode(false);
      setCurrentUser(null);
      console.log(`Utilisateur avec l'ID: ${currentUser._id} modifié`);
    } catch (error) {
      console.error('Erreur lors de la mise à jour de l\'utilisateur', error);
    }
  };

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get('http://localhost:8000/users/all/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,  // Assurez-vous que le token JWT est stocké dans localStorage
          }
        });

        // Filtrer les utilisateurs pour ne garder que ceux avec les rôles "étudiant" ou "bibliothécaire"
        const usersList = response.data.users.filter(user => user.role === 'étudiant' || user.role === 'bibliothécaire');
        
        setUsers(usersList); // Stocker les utilisateurs
      } catch (error) {
        setError('Erreur lors du chargement des utilisateurs');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) return <p>Chargement...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="users-table-container">
      <h1>Liste des utilisateurs</h1>
      
      {/* Bouton pour naviguer vers la page de création */}
      <button onClick={() => navigate('/create')}>Ajouter utilisateur</button>

      {editMode ? (
        <div className="edit-form">
          <h2>Modifier l'utilisateur</h2>
          <input
            type="text"
            value={currentUser.username} // Affichage du username dans l'input
            onChange={(e) => setCurrentUser({ ...currentUser, username: e.target.value })} // Mise à jour du username
            placeholder="Nom d'utilisateur"
          />
          <input
            type="email"
            value={currentUser.email}
            onChange={(e) => setCurrentUser({ ...currentUser, email: e.target.value })}
            placeholder="Email"
          />
          
          {/* Afficher "Université" et "Spécialité" seulement pour les étudiants */}
          {currentUser.role !== 'bibliothécaire' && (
            <>
              <input
                type="text"
                value={currentUser.university}
                onChange={(e) => setCurrentUser({ ...currentUser, university: e.target.value })}
                placeholder="Université"
              />
              <input
                type="text"
                value={currentUser.speciality}
                onChange={(e) => setCurrentUser({ ...currentUser, speciality: e.target.value })}
                placeholder="Spécialité"
              />
            </>
          )}

          {/* Le rôle est affiché en mode lecture uniquement (non modifiable) */}
          <p>Rôle: {currentUser.role}</p>

          <button onClick={handleSaveEdit}>Sauvegarder</button>
          <button onClick={handleCancelEdit}>Annuler</button>
        </div>
      ) : (
        <table className="users-table">
          <thead>
            <tr>
              <th>Nom d'utilisateur</th>
              <th>Email</th>
              <th>Université</th>
              <th>Spécialité</th>
              <th>Rôle</th> {/* Nouvelle colonne pour le rôle */}
              <th>Actions</th> {/* Ajout d'une colonne pour les actions */}
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user._id}>
                <td>{user.username}</td>
                <td>{user.email}</td>
                <td>{user.role !== 'bibliothécaire' ? user.university : '-'}</td> {/* Affiche "-" pour bibliothécaire */}
                <td>{user.role !== 'bibliothécaire' ? user.speciality : '-'}</td> {/* Affiche "-" pour bibliothécaire */}
                <td>{user.role}</td> {/* Affichage du rôle */}
                <td>
                  {/* Boutons d'action */}
                  <button className="buttonuserlist" onClick={() => handleEdit(user._id)}>Modifier</button>
                  <button onClick={() => handleDelete(user._id)}>Supprimer</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default UsersTable;
