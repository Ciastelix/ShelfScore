import { render } from '@testing-library/react';

import PaginatedList from './PaginatedList';

describe('PaginatedList', () => {
  it('should render successfully', () => {
    const { baseElement } = render(<PaginatedList />);
    expect(baseElement).toBeTruthy();
  });
});
