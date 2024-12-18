import styles from './home.module.scss';
import Cookies from 'universal-cookie';
const cookies = new Cookies(null, { path: '/' });

export function Home() {
  return (
    <div className={styles['container']}>
      <h1>Welcome to Home!</h1>
    </div>
  );
}

export default Home;
