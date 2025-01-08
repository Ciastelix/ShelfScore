import styles from './profile.module.scss';
import { useParams } from 'react-router';
import { useEffect, useState } from 'react';
import axios from 'axios';

export function Profile() {
  const { id } = useParams();

  const [user, setUser] = useState<any>({});
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    axios.get(`http://localhost:8000/users/${id}`).then((response) => {
      setUser(response.data);
      setLoading(false);
    });
  }, [id]);

  return (
    <div className={styles['profile-container']}>
      <div className={styles['left-container']}>
        {loading ? (
          <div>Loading...</div>
        ) : (
          <div>
            <img src={`/images/profiles/${user.picture}`} alt="Profile" />
            <h1>{user.username}</h1>
            <p>{user.email}</p>
          </div>
        )}
      </div>
      <div className={styles['center-container']}>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam non
          urna vitae libero bibendum tincidunt. Integer nec odio nec nulla
          facilisis tincidunt.
        </p>
      </div>
      <div className={styles['right-container']}>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam non
          urna vitae libero bibendum tincidunt. Integer nec odio nec nulla
          facilisis tincidunt.
        </p>
      </div>
    </div>
  );
}

export default Profile;
