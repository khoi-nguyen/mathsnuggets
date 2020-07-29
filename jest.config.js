module.exports = {
  moduleFileExtensions: [
    'js',
    'vue'
  ],
  moduleNameMapper: {
    '.*\\.(css)$': 'identity-obj-proxy'
  },
  transform: {
    '.*\\.(js)$': 'babel-jest',
    '.*\\.(vue)$': 'vue-jest'
  },
  setupFiles: [
    'mock-local-storage',
    'regenerator-runtime/runtime'
  ],
  coverageDirectory: './coverage/',
  collectCoverage: true
}
