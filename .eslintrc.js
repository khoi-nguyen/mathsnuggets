module.exports = {
  env: {
    browser: true,
    es6: true
  },
  extends: [
    'plugin:jest/recommended',
    'plugin:vue/essential',
    'standard'
  ],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly'
  },
  parserOptions: {
    ecmaVersion: 11,
    sourceType: 'module'
  },
  plugins: [
    'jest',
    'vue'
  ],
  rules: {
  }
}
