import { useState, useRef, useEffect } from 'react';
import styles from './navbar.module.scss';
import { Login } from '../login/login';
import Cookies from 'universal-cookie';
import axios from 'axios';
import { Link } from 'react-router';

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [fadeOut, setFadeOut] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState<string | undefined>(undefined);
  const loginRef = useRef<HTMLDivElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const [userId, setUserId] = useState('');
  const cookies = new Cookies(null, { path: '/' });
  const [imagePath, setImagePath] = useState('/images/profiles/default.png');

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const logout = async () => {
    cookies.remove('token');
    setToken(undefined);
    setUserId('');
    window.location.replace('/');
  };

  const toggleLogin = (e: React.MouseEvent) => {
    e.preventDefault();

    if (showLogin) {
      setFadeOut(true);
      setTimeout(() => {
        setShowLogin(false);
        setFadeOut(false);
      }, 500);
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
      }, 500);
    }
    if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    if (showLogin || isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showLogin, isOpen]);

  useEffect(() => {
    if (showLogin && loginRef.current) {
      const loginLink = document.querySelector('a[href="#login"]');
      if (loginLink) {
        const rect = loginLink.getBoundingClientRect();
        const loginContainer = loginRef.current;
        loginContainer.style.top = `${rect.bottom + window.scrollY}px`;
        loginContainer.style.left = `${rect.left + window.scrollX}px`;

        const containerRect = loginContainer.getBoundingClientRect();
        if (containerRect.right > window.innerWidth) {
          loginContainer.style.left = `${
            window.innerWidth - containerRect.width
          }px`;
        }
      }
    }
  }, [showLogin]);

  useEffect(() => {
    const fetchUserData = async () => {
      const token = cookies.get('token');
      setToken(token);
      try {
        const res = await axios.get('http://localhost:8000/users/me/token', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setUserId(res.data.user.id);
        setImagePath(
          res.data.user.picture
            ? `/images/profiles/${res.data.user.picture}`
            : '/images/profiles/default.png'
        );
      } catch (err) {
        console.log(err);
      }
    };

    fetchUserData();
  }, [cookies]);

  const handleLoginSuccess = () => {
    setFadeOut(true);
    setTimeout(() => {
      setShowLogin(false);
      setFadeOut(false);
      window.location.replace('/');
    }, 500);
  };

  return (
    <>
      <nav className={styles['navbar']}>
        <Link to="/" className={styles['logo']}>
          ShelfScore
        </Link>
        <div
          className={`${styles['menu']} ${isOpen ? styles['active'] : ''}`}
          ref={menuRef}
        >
          {!token ? (
            <>
              <Link to="#login" onClick={toggleLogin}>
                Login
              </Link>
              <Link to="/register">Register</Link>
            </>
          ) : (
            <>
              <Link
                to={`/profile/${userId}`}
                className={styles['profile-link']}
              >
                <img src={imagePath} alt="Profile" /> Profile
              </Link>
              <Link to="/books">Books</Link>
              <Link to="/authors">Authors</Link>
              <Link to="#logout" onClick={logout}>
                Logout
              </Link>
            </>
          )}
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
              onLoginSuccess={handleLoginSuccess}
            />
          </div>
        </div>
      )}
    </>
  );
}

export default Navbar;
