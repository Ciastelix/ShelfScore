import { ChangeEvent, useState } from 'react';
import styles from './login.module.scss';
import axios from 'axios';
import Cookies from 'universal-cookie';
import { toast } from 'react-toastify';

interface LoginProps {
  email: string;
  password: string;
  setEmail: (email: string) => void;
  setPassword: (password: string) => void;
  onLoginSuccess: () => void;
}

export function Login({
  email,
  password,
  setEmail,
  setPassword,
  onLoginSuccess,
}: LoginProps) {
  const [loading, setLoading] = useState(false);

  const handleEmailChange = (e: ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const cookies = new Cookies(null, { path: '/' });

  const login = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post(
        'http://localhost:8000/users/login',
        {
          username: email,
          password: password,
        },
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );
      if (res.status === 200) {
        console.log(res);
        cookies.set('token', res.data.access_token);
        onLoginSuccess();
      }
    } catch (err) {
      toast.error('Username or password is incorrect!');
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles['login-form']}>
      {loading && (
        <div className={styles['loading-overlay']}>
          <div className={styles['spinner']}></div>
        </div>
      )}
      <form>
        <div className={styles['form-group']}>
          <input
            type="email"
            id="email"
            name="email"
            placeholder=" "
            value={email}
            onChange={handleEmailChange}
            required
          />
          <label htmlFor="email">Email</label>
        </div>
        <div className={styles['form-group']}>
          <input
            type="password"
            id="password"
            name="password"
            placeholder=" "
            value={password}
            onChange={handlePasswordChange}
            required
          />
          <label htmlFor="password">Password</label>
        </div>

        <div className={styles['form-actions']}>
          <div className={styles['remember-me']}>
            <input type="checkbox" id="remember-me" name="remember-me" />
            <label htmlFor="remember-me">Remember me</label>
          </div>

          <button type="submit" onClick={login} disabled={loading}>
            Login
          </button>
        </div>

        <div className={styles['forgot-password']}>
          <a href="/forgot-password">Forgot password?</a>
        </div>
      </form>
    </div>
  );
}

export default Login;
