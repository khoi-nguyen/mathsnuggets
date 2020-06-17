export async function api (url, payload = false) {
  const method = payload ? 'POST' : 'GET'
  const obj = { method: method }
  if (method === 'POST') {
    obj.headers = { 'Content-Type': 'application/json' }
    obj.body = JSON.stringify(payload)
  }
  return await fetch(`/api/${url}`, obj).then(r => r.json())
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
      url += char + key + "=" + encodeURIComponent(payload[key]);
      char = '&'
    }
   }
  fetch(url, obj).then(r => r.json()).then(callback)
}

export function getComponentList (callback) {
  callApi('/api/widgets', 'GET', callback)
}

export function getComponentFields (path, callback) {
  callApi(`/api/widgets/${path}`, 'GET', callback)
}

export function validateForm (widget, payload, callback) {
  callApi(`/api/widgets/${widget}`, 'GET', callback, payload)
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
