import { afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';

afterEach(() => {
  cleanup();
});

vi.mock('axios', () => {
  const axiosMock: any = {
    get: vi.fn().mockResolvedValue({ data: {} }),
    post: vi.fn().mockResolvedValue({ data: {} }),
    put: vi.fn().mockResolvedValue({ data: {} }),
    delete: vi.fn().mockResolvedValue({ data: {} }),
    interceptors: { request: { use: vi.fn() }, response: { use: vi.fn() } },
    isAxiosError: () => true,
  };
  axiosMock.create = vi.fn(() => axiosMock);
  return { default: axiosMock, ...axiosMock };
});

if (!(globalThis as any).fetch) {
  (globalThis as any).fetch = vi.fn(() =>
    Promise.resolve({ ok: true, json: async () => ({}) })
  ) as any;
}