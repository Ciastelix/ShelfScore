import styles from './profile.module.scss';
import { useParams } from 'react-router';
import { useEffect, useState } from 'react';
import axios from 'axios';

export function Profile() {
  const { id } = useParams();

  const [user, setUser] = useState<any>({});
  const [loading, setLoading] = useState(true);
  const [books, setBooks] = useState<any[]>([]);

  async function fetchBooks() {
    const response = await axios.get('http://localhost:8000/users/books-read', {
      headers: {
        'Content-Type': 'application/json',
      },
      params: {
        user_id: id,
      },
    });
    setBooks(response.data);
  }

  useEffect(() => {
    axios.get(`http://localhost:8000/users/u/${id}`).then(async (response) => {
      setUser(response.data);
      setLoading(false);
      await fetchBooks();
    });
  }, [id]);

  const recentBooks = books.slice(0, 3);

  return (
    <div className={styles['profile-container']}>
      <div className={styles['left-container']}>
        {loading ? (
          <div>Loading...</div>
        ) : (
          <div>
            <img src={`/images/profiles/${user.picture}`} alt="Profile" />
            <h1>{user.username}</h1>
            <p>{user.email}</p>
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
          <a href="#" className={styles['show-more-link']}>
            Show more read books ({books.length - 3})
          </a>
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
