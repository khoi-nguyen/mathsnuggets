export async function api (url, method = 'GET', payload = false, cache = true) {
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
    const cached = sessionStorage.getItem(sessionKey)
    if (cached !== null) {
      return JSON.parse(cached)
    }
  }
  const data = await fetch(`/api/${url}`, obj).then(r => r.json())
  if (method === 'GET' && cache) {
    sessionStorage.setItem(sessionKey, JSON.stringify(data))
  }
  return data
}

function callApi (url, method, callback, payload) {
  const obj = { method: method }
  if (method === 'POST') {
    obj.headers = { 'Content-Type': 'application/json' }
    obj.body = JSON.stringify(payload)
  }
  if (method === 'GET' && payload) {
    let char = '?'
    for (var key in payload) {
      url += char + key + '=' + encodeURIComponent(payload[key])
      char = '&'
    }
  }
  fetch(url, obj).then(r => r.json()).then(callback)
}

export function getSlideshowList (callback) {
  callApi('/api/slideshows', 'GET', callback)
}

export function getSlideshow (id, callback) {
  callApi(`/api/slideshows/${id}`, 'GET', callback)
}

export function saveSlideshow (id, payload, callback) {
  callApi(`/api/slideshows/${id}`, 'POST', callback, payload)
}

export function login (payload, callback) {
  callApi('/api/auth/login', 'POST', callback, payload)
}

export function isLoggedIn (callback) {
  callApi('/api/auth/login', 'GET', callback)
}

export function logout (callback) {
  callApi('/api/auth/logout', 'GET', callback)
}
