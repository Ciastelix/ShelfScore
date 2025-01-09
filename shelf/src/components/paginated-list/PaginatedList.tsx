import React, { useEffect, useState, useCallback } from 'react';
import styles from './PaginatedList.module.scss';
import { Link } from 'react-router';

interface PaginatedListProps<T> {
  items: T[];
  linkPrefix: string;
  searchKeys: (keyof T)[];
  itemsPerPage?: number;
}

export function PaginatedList<T extends { id: string }>({
  items,
  linkPrefix,
  searchKeys,
  itemsPerPage = 35,
}: PaginatedListProps<T>) {
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedQuery, setDebouncedQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);

  const debounce = (func: Function, delay: number) => {
    let timer: NodeJS.Timeout;
    return (...args: any[]) => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        func(...args);
      }, delay);
    };
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let query = e.target.value;

    query = query.replace(/^\s+/, '').replace(/\s{2,}$/, ' ');
    setSearchQuery(query);
    setCurrentPage(1);
  };

  const debouncedSearch = useCallback(
    debounce((query: string) => {
      setDebouncedQuery(query);
    }, 300),
    []
  );

  useEffect(() => {
    if (searchQuery.length >= 3) {
      debouncedSearch(searchQuery);
    } else {
      setDebouncedQuery('');
    }
  }, [searchQuery, debouncedSearch]);

  const isString = (value: any): value is string => {
    return typeof value === 'string' || value instanceof String;
  };

  const filteredItems = items.filter((item) =>
    searchKeys.some((key) => {
      const value = item[key];
      return (
        isString(value) &&
        value.toLowerCase().includes(debouncedQuery.toLowerCase())
      );
    })
  );

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredItems.slice(indexOfFirstItem, indexOfLastItem);

  const totalPages = Math.ceil(filteredItems.length / itemsPerPage);

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
      <input
        type="text"
        placeholder="Search..."
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
          {currentItems.map((item) => (
            <Link
              to={`${linkPrefix}/${item.id}`}
              key={item.id}
              className={styles['card-link']}
            >
              <div className={styles['card']}>
                {searchKeys.map((key, index) => (
                  <p
                    key={key as string}
                    className={index === 0 ? styles['bold'] : ''}
                  >
                    {String(item[key])}
                  </p>
                ))}
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
