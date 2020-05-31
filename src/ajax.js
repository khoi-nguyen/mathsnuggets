export function getComponentList (callback) {
  fetch('/_components', { method: 'GET' }).then(r => r.json()).then(callback)
}

export function getSlideShow (callback) {
  fetch('/_slideshow', { method: 'GET' }).then(r => r.json()).then(callback)
}

export function getComponentFields (path, callback) {
  fetch('/_form/' + path, { method: 'GET' }).then(r => r.json()).then(callback)
}

export function validateForm (path, formData, callback) {
  fetch('/_form/' + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formData) }).then(r => r.json()).then(callback)
}

export function validateField (field, fieldData, callback) {
  fetch('/_field/' + field, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(fieldData) }).then(r => r.json()).then(callback)
}
