import React, { useEffect, useState } from 'react';
import styles from './authors.module.scss';
import axios from 'axios';
import { Link } from 'react-router';

interface Author {
  id: string;
  name: string;
  surname: string;
  description: string;
}

export function Authors() {
  const [authors, setAuthors] = useState<Author[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const authorsPerPage = 35;

  useEffect(() => {
    axios.get('http://localhost:8000/authors').then((response) => {
      setAuthors(response.data);
    });
  }, []);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
    setCurrentPage(1); // Reset to the first page on search
  };

  const filteredAuthors = authors.filter((author) =>
    `${author.name} ${author.surname}`
      .toLowerCase()
      .includes(searchQuery.toLowerCase())
  );

  // Calculate the authors to display on the current page
  const indexOfLastAuthor = currentPage * authorsPerPage;
  const indexOfFirstAuthor = indexOfLastAuthor - authorsPerPage;
  const currentAuthors = filteredAuthors.slice(
    indexOfFirstAuthor,
    indexOfLastAuthor
  );

  const totalPages = Math.ceil(filteredAuthors.length / authorsPerPage);

  const handleNextPage = (e: React.MouseEvent<HTMLDivElement>) => {
    if (currentPage < totalPages) {
      createRipple(e);
      setTimeout(() => {
        setCurrentPage(currentPage + 1);
      }, 200);
    }
  };

  const handlePreviousPage = (e: React.MouseEvent<HTMLDivElement>) => {
    if (currentPage > 1) {
      createRipple(e);
      setTimeout(() => {
        setCurrentPage(currentPage - 1);
      }, 200);
    }
  };

  const createRipple = (e: React.MouseEvent<HTMLDivElement>) => {
    const rippleContainer = e.currentTarget.querySelector(
      `.${styles['ripple-container']}`
    );
    const ripple = document.createElement('span');
    const diameter = Math.max(
      rippleContainer!.clientWidth,
      rippleContainer!.clientHeight
    );
    const radius = diameter / 2;

    ripple.style.width = ripple.style.height = `${diameter}px`;
    ripple.style.left = `${
      e.clientX - rippleContainer!.getBoundingClientRect().left - radius
    }px`;
    ripple.style.top = `${
      e.clientY - rippleContainer!.getBoundingClientRect().top - radius
    }px`;
    ripple.classList.add(styles['ripple']);

    const rippleElement = rippleContainer!.getElementsByClassName(
      styles['ripple']
    )[0];
    if (rippleElement) {
      rippleElement.remove();
    }

    rippleContainer!.appendChild(ripple);
  };

  return (
    <div className={styles['container']}>
      <h1>Authors</h1>

      <input
        type="text"
        placeholder="Search by name or surname"
        value={searchQuery}
        onChange={handleSearchChange}
        className={styles['search-input']}
      />
      <div
        className={styles['arrow-container']}
        onClick={handlePreviousPage}
        style={{ visibility: currentPage === 1 ? 'hidden' : 'visible' }}
      >
        <span className="material-symbols-outlined">arrow_back_ios</span>
        <div className={styles['ripple-container']}></div>
      </div>
      <div className={styles['pagination-container']}>
        <div className={styles['cards-container']}>
          {currentAuthors.map((author) => (
            <Link
              to={`/author/${author.id}`}
              key={author.id}
              className={styles['card-link']}
            >
              <div className={styles['card']}>
                <h2>
                  {author.name} {author.surname}
                </h2>
                <p>{author.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
      <div
        className={styles['arrow-container']}
        onClick={handleNextPage}
        style={{
          visibility: currentPage === totalPages ? 'hidden' : 'visible',
        }}
      >
        <span className="material-symbols-outlined">arrow_forward_ios</span>
        <div className={styles['ripple-container']}></div>
      </div>
    </div>
  );
}

export default Authors;
