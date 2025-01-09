import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { PaginatedList } from '../paginated-list/PaginatedList';

interface Author {
  id: string;
  name: string;
  surname: string;
  description: string;
}

export function Authors() {
  const [authors, setAuthors] = useState<Author[]>([]);

  useEffect(() => {
    axios.get('http://localhost:8000/authors').then((response) => {
      setAuthors(response.data);
    });
  }, []);

  return (
    <PaginatedList
      items={authors}
      linkPrefix="/author"
      searchKeys={['name', 'surname']}
    />
  );
}

export default Authors;
