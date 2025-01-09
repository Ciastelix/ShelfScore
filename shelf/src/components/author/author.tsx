import styles from './author.module.scss';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router';

export function Author() {
  const { id } = useParams();
  const [author, setAuthor] = useState<any>({});

  useEffect(() => {
    axios.get(`http://localhost:8000/authors/${id}`).then((response) => {
      setAuthor(response.data);
    });
  }, [id]);

  return (
    <div className={styles['container']}>
      <h1>
        {author.name} {author.surname}
      </h1>
      <p>{author.description}</p>
    </div>
  );
}

export default Author;
