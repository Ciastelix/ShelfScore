// Uncomment this line to use CSS modules
// import styles from './app.module.scss';
import styles from './app.module.scss';

import Navbar from '../components/navbar/navbar';
import Home from '../components/home/home';
export function App() {
  return (
    <div className={styles['content']}>
      <Navbar />

      <Home />
    </div>
  );
}

export default App;
