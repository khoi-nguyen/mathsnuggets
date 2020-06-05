export function getComponentList (callback) {
  fetch('/api/widgets', { method: 'GET' }).then(r => r.json()).then(callback)
}

export function getComponentFields (path, callback) {
  fetch('/api/widgets/' + path, { method: 'GET' }).then(r => r.json()).then(callback)
}

export function validateForm (path, formData, callback) {
  fetch('/api/widgets/' + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formData) }).then(r => r.json()).then(callback)
}

export function validateField (field, fieldData, callback) {
  fetch('/api/fields/' + field, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(fieldData) }).then(r => r.json()).then(callback)
}

export function getSlideshow (callback) {
  fetch('/api/slideshows', { method: 'GET' }).then(r => r.json()).then(callback)
}

export function saveSlideshow (payload, callback) {
  fetch('/api/slideshows/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }).then(r => r.json()).then(callback)
}
