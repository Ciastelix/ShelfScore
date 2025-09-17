import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router';

import App from './app';

const renderWithRouter = (ui: any) => render(<MemoryRouter>{ui}</MemoryRouter>);

describe('App', () => {
  it('should render successfully', () => {
    const { baseElement } = renderWithRouter(<App />);
    expect(baseElement).toBeTruthy();
  });

  it('should show the Home heading on root route', () => {
    const { getByText } = renderWithRouter(<App />);
    expect(getByText(/Welcome to Home!/i)).toBeTruthy();
  });
});
