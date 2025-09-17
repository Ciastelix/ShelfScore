import styles from './profile.module.scss';
import { useParams } from 'react-router';
import { useEffect, useState, useMemo, useCallback } from 'react';
import axios from 'axios';
import Cookies from 'universal-cookie';

type UserProfile = {
  id: string;
  username: string;
  email: string;
  picture?: string;
};

type ReadBook = {
  id: string;
  title: string;
  image: string;
  author_name: string;
  author_surname: string;
};

export function Profile() {
  const { id } = useParams();
  const cookies = useMemo(() => new Cookies(), []);

  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [books, setBooks] = useState<ReadBook[]>([]);
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);

  const fetchBooks = useCallback(async () => {
    if (!id) return;
    try {
      const response = await axios.get('http://localhost:8000/users/books-read', {
        headers: { 'Content-Type': 'application/json' },
        params: { user_id: id },
      });
      setBooks(response.data);
    } catch (error) {
      console.error('Error fetching books:', error);
    }
  }, [id]);

  useEffect(() => {
    if (!id) {
      setLoading(false);
      return;
    }
    const fetchData = async () => {
      try {
        const token = cookies.get('token') || localStorage.getItem('token');

        if (token) {
          const response = await axios.get('http://localhost:8000/users/me/token', {
            headers: { Authorization: `Bearer ${token}` },
          });
          setCurrentUserId(response.data.user.id as string);
        }

        const profileResponse = await axios.get(
          `http://localhost:8000/users/u/${id}`
        );
        setUser(profileResponse.data);
        setLoading(false);

        await fetchBooks();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [id, cookies, fetchBooks]);

  const recentBooks = books.slice(0, 3);

  const handleEditProfile = () => {
    window.location.href = `/edit-profile/${id}`;
  };

  return (
    <div className={styles['profile-container']}>
      <div className={styles['left-container']}>
        {loading ? (
          <div>Loading...</div>
        ) : (
          <div>
            <img src={`/images/profiles/${user?.picture}`} alt="Profile" />
            <h1>{user?.username}</h1>
            <p>{user?.email}</p>
            {currentUserId === id && (
              <button
                className={styles['edit-profile-button']}
                onClick={handleEditProfile}
              >
                Edit Profile
              </button>
            )}
          </div>
        )}
      </div>
      <div className={styles['center-container']}>
        <h2>Recently Read Books</h2>
        <div className={styles['recent-books-container']}>
          {recentBooks.map((book) => (
            <div key={book.id} className={styles['book-card']}>
              <img src={`/${book.image}`} alt={book.title} />
              <h3>{book.title}</h3>
              <p>
                {book.author_name} {book.author_surname}
              </p>
            </div>
          ))}
        </div>
        {books.length > 3 && (
          <button type="button" className={styles['show-more-link']}>
            Show more read books ({books.length - 3})
          </button>
        )}
      </div>
      <div className={styles['right-container']}>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam non
          urna vitae libero bibendum tincidunt. Integer nec odio nec nulla
          facilisis tincidunt.
        </p>
      </div>
    </div>
  );
}

export default Profile;
