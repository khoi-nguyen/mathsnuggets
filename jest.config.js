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
  coverageDirectory: './coverage/',
  collectCoverage: true
}
