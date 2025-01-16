import styles from './books.module.scss';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { PaginatedList } from '../paginated-list/PaginatedList';

interface Book {
  author_id: string;
  id: string;
  title: string;
  image: string;
}

export function Books() {
  const [books, setBooks] = useState<Book[]>([]);

  useEffect(() => {
    axios.get('http://localhost:8000/books').then((response) => {
      setBooks(response.data);
    });
  }, []);

  return (
    <PaginatedList items={books} linkPrefix="/book" searchKeys={['title']} />
  );
}

export default Books;
