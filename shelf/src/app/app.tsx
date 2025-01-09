// Uncomment this line to use CSS modules
// import styles from './app.module.scss';
import styles from './app.module.scss';

import Navbar from '../components/navbar/navbar';
import Home from '../components/home/home';
import { useEffect, useState } from 'react';
import { Route, Routes } from 'react-router';
import Login from '../components/login/login';
import Profile from '../components/profile/profile';
import Register from '../components/register/register';
import { ToastContainer } from 'react-toastify';
import Authors from '../components/authors/authors';
import Author from '../components/author/author';
import Books from '../components/books/books';
import Book from '../components/book/book';
export function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fadeOut, setFadeOut] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const handleLoginSuccess = () => {
    setFadeOut(true);
    setTimeout(() => {
      setShowLogin(false);
      setFadeOut(false);
    }, 500);
  };
  // TODO create generic list component to display authors and books
  useEffect(() => {
    const handleBeforeUnload = (event: any) => {
      console.log('Page is about to be closed!');

      event.preventDefault();
      event.returnValue = '';
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
              onLoginSuccess={handleLoginSuccess}
            />
          }
        />
        <Route path="/register" element={<Register />} />
        <Route path="/profile/:id" element={<Profile />}></Route>
        <Route path="/authors" element={<Authors />} />
        <Route path="/author/:id" element={<Author />} />
        <Route path="/books" element={<Books />} />
        <Route path="/book/:id" element={<Book />} />
        <Route path="*" element={<h1>Page not found</h1>} />
      </Routes>
      <ToastContainer
        position="top-center"
        autoClose={5000}
        hideProgressBar
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored"
      />
    </div>
  );
}

export default App;
