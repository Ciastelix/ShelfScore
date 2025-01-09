import styles from './book.module.scss';

export function Book() {
  return (
    <div className={styles['container']}>
      <h1>Welcome to Book!</h1>
    </div>
  );
}

export default Book;
