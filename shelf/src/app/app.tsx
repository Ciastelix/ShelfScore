// Uncomment this line to use CSS modules
// import styles from './app.module.scss';
import styles from './app.module.scss';

import Navbar from '../components/navbar/navbar';
import Home from '../components/home/home';
import { useEffect, useState } from 'react';
import { Route, Routes } from 'react-router';
import Login from '../components/login/login';

export function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => {
    const handleBeforeUnload = (event: any) => {
      // Custom logic to run before the page is closed
      console.log('Page is about to be closed!');

      // Optional: Show a confirmation dialog
      event.preventDefault();
      event.returnValue = ''; // Some browsers require returnValue to be set.
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  return (
    <div className={styles['content']}>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/login"
          element={
            <Login
              email={email}
              password={password}
              setEmail={setEmail}
              setPassword={setPassword}
            />
          }
        />
      </Routes>
    </div>
  );
}

export default App;
