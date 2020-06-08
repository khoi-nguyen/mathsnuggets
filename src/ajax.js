function callApi (url, method, callback, payload) {
  const obj = { method: method }
  if (method === 'POST') {
    obj.headers = { 'Content-Type': 'application/json' }
    obj.body = JSON.stringify(payload)
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
  callApi(`/api/widgets/${widget}`, 'POST', callback, payload)
}

export function validateField (field, payload, callback) {
  callApi(`/api/fields/${field}`, 'POST', callback, payload)
}

export function getSlideshow (callback) {
  callApi('/api/slideshows', 'GET', callback)
}

export function saveSlideshow (payload, callback) {
  callApi('/api/slideshows/save', 'POST', callback, payload)
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
