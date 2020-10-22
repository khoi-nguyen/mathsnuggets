export default async function api (url, method = 'GET', payload = false, cache = false) {
  if (payload.src) {
    method = 'POST'
  }
  const obj = { method: method }
  if (method === 'POST') {
    obj.headers = { 'Content-Type': 'application/json' }
    obj.body = JSON.stringify(payload)
  }
  let sessionKey = url
  if (method === 'GET') {
    if (payload) {
      let char = '?'
      for (var key in payload) {
        url += char + key + '=' + encodeURIComponent(payload[key])
        sessionKey += char + key + '=' + payload[key]
        char = '&'
      }
    }
    const cached = localStorage.getItem(sessionKey)
    if (cached !== null && cache) {
      return JSON.parse(cached)
    }
  }
  const data = await fetch(`/api/${url}`, obj).then(r => r.json())
  if (cache) {
    localStorage.setItem(sessionKey, JSON.stringify(data))
  }
  return data
}
