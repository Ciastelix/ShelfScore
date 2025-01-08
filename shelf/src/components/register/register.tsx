import { ChangeEvent, useState } from 'react';
import styles from './register.module.scss';
import axios from 'axios';
import { toast } from 'react-toastify';

export function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [retypePassword, setRetypePassword] = useState('');
  const [loading, setLoading] = useState(false);

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

  const register = async (e: any) => {
    e.preventDefault();
    if (password !== retypePassword) {
      toast.error('Passwords do not match!');
      setRetypePassword('');
      setPassword('');
      return;
    }
    setLoading(true);
    try {
      const res = await axios.post(
        'http://localhost:8000/users/',
        {
          username: username,
          email: email,
          password: password,
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      if (res.status === 201) {
        toast.success('User registered successfully! You can now login.');
        setTimeout(() => {
          window.location.replace('/');
        }, 5000);
      }
    } catch (err) {
      toast.error('Error registering user');
      console.log(err);
      setRetypePassword('');
      setPassword('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles['register-container']}>
      {loading && (
        <div className={styles['loading-overlay']}>
          <div className={styles['spinner']}></div>
        </div>
      )}
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
            <button type="submit" onClick={register} disabled={loading}>
              Register
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Register;
