import styles from './book.module.scss';
import { useParams } from 'react-router';
import { useEffect, useState } from 'react';
import axios from 'axios';

export function Book() {
  const { id } = useParams();
  const [book, setBook] = useState<any>({});

  useEffect(() => {
    axios.get(`http://localhost:8000/books/${id}`).then((response) => {
      setBook(response.data);
    });
  }, [id]);

  return (
    <div className={styles['container']}>
      <h1>{book.title}</h1>
      <p>{book.description}</p>
    </div>
  );
}

export default Book;
