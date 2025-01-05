import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import Button from "../../components/button/Button";
import Popup from "../../components/popup/Popup";
import Modal from "../../components/modal/Modal"; // Importe o componente de modal personalizado
import TextInput from "../../components/textInput/TextInput";
import { useNavigate } from "react-router-dom";
import "./Book.css";

const Book = () => {
  const { bookId } = useParams();
  const [book, setBook] = useState(null);
  const [publisher, setPublisher] = useState(null);
  const [isInBookshelf, setIsInBookshelf] = useState(false);
  const [isIsMineBook, setIsMineBook] = useState(false);
  const [popupMessage, setPopupMessage] = useState("");
  const [popupType, setPopupType] = useState("");
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false); // Estado para controlar a exibição do modal de edição
  const [editedBook, setEditedBook] = useState({
    title: "",
    author: "",
    link: "",
  }); // Estado para armazenar os campos editados do livro
  const token = localStorage.getItem("token");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBookDetail = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/${bookId}/`);
        const bookData = response.data;
        setBook(bookData);

        // Fetch user details using post_by ID
        const publisherResponse = await axios.get(
          `http://localhost:8000/user/${bookData.post_by}/`
        );
        setPublisher(publisherResponse.data);

        // Fetch bookshelf and check if the book is in the bookshelf
        if (token != null) {
          const bookshelfResponse = await axios.get(
            `http://localhost:8000/bookshelf/list/`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );

          const userResponse = await axios.get(
            `http://localhost:8000/profile/`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );

          const booksInShelf = bookshelfResponse.data;
          setIsInBookshelf(booksInShelf.includes(bookId));

          const userData = userResponse.data;
          if (bookData.post_by === userData._id) {
            setIsMineBook(true);
          }
        }
      } catch (error) {
        console.error("Error fetching book or user details:", error);
      }
    };

    fetchBookDetail();
  }, [bookId, token, showEditModal]);

  const handleClosePopup = () => {
    setPopupMessage("");
    setPopupType("");
  };

  async function toggleBookshelf() {
    try {
      if (token != null) {
        if (isInBookshelf) {
          // Remove from shelf
          await axios.delete(
            `http://localhost:8000/bookshelf/${bookId}/remove/`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          setPopupMessage("Removed from shelf!");
        } else {
          // Add to shelf
          await axios.post(
            `http://localhost:8000/bookshelf/${bookId}/add/`,
            {},
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          setPopupMessage("Added to shelf!");
        }
        setIsInBookshelf(!isInBookshelf);
        setPopupType(isInBookshelf ? "warning" : "success");
      } else {
        console.log("token missing");
      }
    } catch (error) {
      console.error("Error toggling bookshelf:", error);
      setPopupMessage("Failed to update shelf. Please try again.");
      setPopupType("error");
    }
  }

  // Função para lidar com a exclusão do livro
  const handleDeleteBook = async () => {
    try {
      // Não exibir o modal de exclusão se não houver um token
      if (token == null) {
        console.log("Token missing");
        return;
      }

      // Oculta o modal de exclusão
      setShowDeleteModal(false);

      // Realiza a exclusão do livro
      await axios.delete(`http://localhost:8000/${bookId}/delete/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      // Exibe uma mensagem de sucesso
      setPopupMessage("Book deleted successfully!");
      setPopupType("success");

      setTimeout(() => {
        navigate(-1);
      }, 1000);

      // Redirecionar para uma página de sucesso ou qualquer outra ação necessária após a exclusão
    } catch (error) {
      console.error("Error deleting book:", error);
      setPopupMessage("Failed to delete book. Please try again.");
      setPopupType("error");
    }
  };

  const handleEditBook = async () => {
    try {
      // Crie um objeto vazio para armazenar os campos editados
      const editedFields = {};

      // Verifique cada campo e adicione ao objeto apenas se tiver sido editado
      if (editedBook.title !== book.title) {
        editedFields.title = editedBook.title;
      }
      if (editedBook.author !== book.author) {
        editedFields.author = editedBook.author;
      }
      if (editedBook.link !== book.link) {
        editedFields.link = editedBook.link;
      }

      // Verifica se algum campo foi editado
      if (Object.keys(editedFields).length === 0) {
        setPopupMessage("No changes detected.");
        setPopupType("warning");
        return;
      }

      // Realiza a edição do livro enviando apenas os campos editados
      await axios.put(`http://localhost:8000/${bookId}/edit/`, editedFields, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setShowEditModal(false); // Fecha o modal de edição
      setPopupMessage("Book edited successfully!");
      setPopupType("success");
    } catch (error) {
      console.error("Error editing book:", error);
      setPopupMessage("Failed to edit book. Please try again.");
      setPopupType("error");
    }
  };

  if (!book || !publisher) {
    return <div>Loading...</div>;
  }

  return (
    <div className="book-detail-overlay">
      <div className="book-detail">
        <h2>{book.title}</h2>
        <p>Author: {book.author}</p>
      </div>
      <div className="book-info">
        <div>
          <h2>Book title:</h2>
          <p>{book.title}</p>
        </div>
        <div>
          <h2>Author:</h2>
          <p>{book.author}</p>
        </div>
        <div>
          <h2>Posted by:</h2>
          <p>
            {publisher.username} - {publisher.email}
          </p>
        </div>
      </div>
      <div className="book-buttons">
        <Button
          dark={false}
          text={"Read book"}
          onClick={() => {
            window.open(book.link, "_blank");
          }}
        />
        <Button
          dark={true}
          text={isInBookshelf ? "Remove" : "Save"}
          onClick={() => {
            if (token !== null) {
              toggleBookshelf();
            } else {
              setPopupMessage("Sign in to use the shelf");
              setPopupType("warning");
            }
          }}
          opacity={token ? 1 : 0.4}
        />

        {isIsMineBook ? (
          <>
            <Button
              dark={true}
              text={"Edit"}
              onClick={() => setShowEditModal(true)}
            />
            <Button
              dark={true}
              text={"Delete"}
              onClick={() => setShowDeleteModal(true)}
            />{" "}
            {/* Mostra o modal de exclusão quando o botão "Delete" é clicado */}
          </>
        ) : (
          <></>
        )}
      </div>

      <Popup
        message={popupMessage}
        type={popupType}
        onClose={handleClosePopup}
      />

      {/* Modal de confirmação para exclusão */}
      <Modal
        show={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Confirm Delete"
      >
        <p>Are you sure you want to delete this book?</p>
        <div className="modal-buttons">
          <Button text="Delete" onClick={handleDeleteBook} />
        </div>
      </Modal>

      {/* Modal de edição */}
      <Modal
        show={showEditModal}
        onClose={() => setShowEditModal(false)}
        title="Edit Book"
      >
        <div className="modal-body">
          <TextInput
            placeholder={book.title}
            value={editedBook.title}
            onChange={(e) =>
              setEditedBook({ ...editedBook, title: e.target.value })
            }
            type="text"
          />
          <TextInput
            placeholder={book.author}
            value={editedBook.author}
            onChange={(e) =>
              setEditedBook({ ...editedBook, author: e.target.value })
            }
            type="text"
          />
          <TextInput
            placeholder={book.link}
            value={editedBook.link}
            onChange={(e) =>
              setEditedBook({ ...editedBook, link: e.target.value })
            }
            type="text"
          />
          <Button text="Save Changes" onClick={handleEditBook} />
        </div>
      </Modal>
    </div>
  );
};

export default Book;
