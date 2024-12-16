import styles from './login.module.scss';

export function Login() {
  return (
    <div className={styles['login-form']}>
      <form>
        <div className={styles['form-group']}>
          <input
            type="email"
            id="email"
            name="email"
            placeholder=" "
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
            required
          />
          <label htmlFor="password">Password</label>
        </div>

        <div className={styles['form-actions']}>
          <div className={styles['remember-me']}>
            <input type="checkbox" id="remember-me" name="remember-me" />
            <label htmlFor="remember-me">Remember me</label>
          </div>

          <button type="submit">Login</button>
        </div>

        <div className={styles['forgot-password']}>
          <a href="/forgot-password">Forgot password?</a>
        </div>
      </form>
    </div>
  );
}

export default Login;
