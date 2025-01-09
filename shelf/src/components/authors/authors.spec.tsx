import { render } from '@testing-library/react';

import Authors from './authors';

describe('Authors', () => {
  it('should render successfully', () => {
    const { baseElement } = render(<Authors />);
    expect(baseElement).toBeTruthy();
  });
});
