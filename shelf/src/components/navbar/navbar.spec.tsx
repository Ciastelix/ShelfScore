import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router';

import Navbar from './navbar';

describe('Navbar', () => {
  it('should render successfully', () => {
    const { baseElement } = render(
      <MemoryRouter>
        <Navbar />
      </MemoryRouter>
    );
    expect(baseElement).toBeTruthy();
  });
});
