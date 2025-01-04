import { ChangeEvent, useState } from 'react';
import styles from './register.module.scss';
import axios from 'axios';
import Cookies from 'universal-cookie';

export function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [retypePassword, setRetypePassword] = useState('');

  const handleUsernameChange = (e: ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
  };

  const handleEmailChange = (e: ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handleRetypePasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
    setRetypePassword(e.target.value);
  };

  const cookies = new Cookies(null, { path: '/' });

  const register = async (e: any) => {
    e.preventDefault();
    if (password !== retypePassword) {
      alert('Passwords do not match');
      return;
    }
    try {
      const res = await axios.post(
        'http://localhost:8000/users/register',
        {
          username: username,
          email: email,
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
        window.location.href = '/';
      }
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className={styles['register-form']}>
      <form>
        <div className={styles['form-group']}>
          <input
            type="text"
            id="username"
            name="username"
            placeholder=" "
            value={username}
            onChange={handleUsernameChange}
            required
          />
          <label htmlFor="username">Username</label>
        </div>
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
        <div className={styles['form-group']}>
          <input
            type="password"
            id="retype-password"
            name="retype-password"
            placeholder=" "
            value={retypePassword}
            onChange={handleRetypePasswordChange}
            required
          />
          <label htmlFor="retype-password">Retype Password</label>
        </div>

        <div className={styles['form-actions']}>
          <button type="submit" onClick={register}>
            Register
          </button>
        </div>
      </form>
    </div>
  );
}

export default Register;
