import { useState, useRef, useEffect } from 'react';
import styles from './navbar.module.scss';
import { Login } from '../login/login';

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [fadeOut, setFadeOut] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const loginRef = useRef<HTMLDivElement>(null);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const toggleLogin = (e: React.MouseEvent) => {
    e.preventDefault();
    if (showLogin) {
      setFadeOut(true);
      setTimeout(() => {
        setShowLogin(false);
        setFadeOut(false);
      }, 500); // Match the duration of the fade-out animation
    } else {
      setShowLogin(true);
    }
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (loginRef.current && !loginRef.current.contains(event.target as Node)) {
      setFadeOut(true);
      setTimeout(() => {
        setShowLogin(false);
        setFadeOut(false);
      }, 500); // Match the duration of the fade-out animation
    }
  };

  useEffect(() => {
    if (showLogin) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showLogin]);

  useEffect(() => {
    if (showLogin && loginRef.current) {
      const loginLink = document.querySelector('a[href="#login"]');
      if (loginLink) {
        const rect = loginLink.getBoundingClientRect();
        const loginContainer = loginRef.current;
        loginContainer.style.top = `${rect.bottom + window.scrollY}px`;
        loginContainer.style.left = `${rect.left + window.scrollX}px`;

        // Ensure the login form doesn't overflow the viewport
        const containerRect = loginContainer.getBoundingClientRect();
        if (containerRect.right > window.innerWidth) {
          loginContainer.style.left = `${
            window.innerWidth - containerRect.width
          }px`;
        }
      }
    }
  }, [showLogin]);

  return (
    <>
      <nav className={styles['navbar']}>
        <div className={styles['logo']}>ShelfScore</div>
        <div className={`${styles['menu']} ${isOpen ? styles['active'] : ''}`}>
          <a href="#login" onClick={toggleLogin}>
            Login
          </a>
          <a href="#register">Register</a>
        </div>
        <div className={styles['hamburger']} onClick={toggleMenu}>
          <span></span>
          <span></span>
          <span></span>
        </div>
      </nav>
      {showLogin && (
        <div
          className={`${styles['login-container']} ${
            fadeOut ? styles['fade-out'] : ''
          }`}
          ref={loginRef}
        >
          <div
            className={styles['login-wrapper']}
            onClick={(e) => e.stopPropagation()}
          >
            <Login
              email={email}
              password={password}
              setEmail={setEmail}
              setPassword={setPassword}
            />
          </div>
        </div>
      )}
    </>
  );
}

export default Navbar;
