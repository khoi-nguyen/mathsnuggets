import { enableFetchMocks } from 'jest-fetch-mock'
import api from './ajax'

enableFetchMocks()

describe('API calls', () => {
  beforeEach(() => {
    fetch.resetMocks()
  })

  it('URL should be correct', () => {
    api('widgets/LinearEquation')
    api('fields/Equation', 'GET', { value: 'x', options: [] })
    api('fields/Equation', 'POST', { value: 'x', options: [] })
    expect(fetch.mock.calls[0][0]).toEqual('/api/widgets/LinearEquation')
    expect(fetch.mock.calls[1][0]).toEqual('/api/fields/Equation?value=x&options=')
    expect(fetch.mock.calls[2][0]).toEqual('/api/fields/Equation')
    expect(fetch).toHaveBeenCalledTimes(3)
  })

  it('POST/GET requests should be handled properly', () => {
    api('fields/Equation', 'GET', { value: 'x' })
    api('fields/Equation', 'POST', { value: 'x' })
    expect(fetch.mock.calls[0][1].method).toEqual('GET')
    expect(fetch.mock.calls[1][1].method).toEqual('POST')
    expect(fetch.mock.calls[1][1].headers).toEqual({ 'Content-Type': 'application/json' })
    expect(fetch).toHaveBeenCalledTimes(2)
  })

  it('Requests can be cached', async () => {
    const response = JSON.stringify({ data: '12345' })
    fetch.mockResponse(response)

    await api('fields/Equation', 'GET', { value: 'x' })
    expect(sessionStorage.length).toBe(0)

    await api('fields/Equation', 'POST', { value: 'x' }, true)
    expect(sessionStorage.length).toBe(0)

    await api('fields/Equation', 'GET', { value: 'x' }, true)
    expect(sessionStorage.getItem('fields/Equation?value=x')).toEqual(response)

    await api('fields/Equation', 'GET', { value: 'x' }, true)
    expect(fetch).toHaveBeenCalledTimes(3)
  })
})
