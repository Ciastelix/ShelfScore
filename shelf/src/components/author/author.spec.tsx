import { render } from '@testing-library/react';

import Author from './author';

describe('Author', () => {
  it('should render successfully', () => {
    const { baseElement } = render(<Author />);
    expect(baseElement).toBeTruthy();
  });
});
