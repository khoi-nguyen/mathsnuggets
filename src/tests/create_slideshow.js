const assert = require('assert')
const fetch = require('node-fetch')
const mocha = require('mocha')
const puppeteer = require('puppeteer')

async function selectWidget (page, widget) {
  const identifier = 'section.present .autocomplete input'
  await page.waitFor(identifier)
  await page.click(identifier, { clickCount: 3 })
  await page.keyboard.type(widget)
  const typedValue = await page.$eval(identifier, el => el.value)
  assert.equal(typedValue, widget)
  await page.keyboard.press('Enter')
}

async function fillInField (page, identifier, value, key = 'Tab') {
  await page.waitFor(identifier)
  await page.focus(identifier)
  await page.keyboard.type(value)
  const typedValue = await page.$eval(identifier, el => el.value)
  assert.equal(typedValue, value)
  await page.keyboard.press(key)
  await page.waitForFunction((selector) => !document.querySelector(selector), identifier)
}

async function waitForComputedFields (page) {
  try {
    await page.waitForSelector('.is-danger', { timeout: 500 })
    assert.equal(true, false)
  } catch (error) {
    assert.equal(true, true)
  }
  const identifier = 'span button.computed-field'
  await page.waitFor(identifier)
  await page.click(identifier)
  await page.keyboard.press('ArrowRight')
}

mocha.describe('mathsnuggets', function () {
  let browser
  let page
  this.timeout(100000)

  mocha.before(async function () {
    browser = await puppeteer.launch({ headless: false, args: ['--no-sandbox'] })
    page = await browser.newPage()
  })

  mocha.after(async function () {
    browser.close()
  })

  mocha.it('changing the title', async function () {
    await page.goto('http://localhost:5000/slideshow_builder')
    const identifier = 'section.present .slide-title'

    const checkTitle = async function (assertMethod, string) {
      const title = await page.$eval(identifier, el => el.value)
      assert[assertMethod](title, string)
    }

    await page.waitFor(identifier)
    await page.keyboard.press('Tab')
    await page.keyboard.type('Test')
    await page.keyboard.press('Enter')
    await checkTitle('equal', 'Test')

    await page.click(identifier)
    await page.keyboard.type('Hello')
    await page.keyboard.press('Enter')
    await checkTitle('equal', 'Hello')

    await page.keyboard.press('ArrowRight')
    await checkTitle('notEqual', 'Hello')
    await page.keyboard.press('ArrowLeft')
    await checkTitle('equal', 'Hello')
  })

  mocha.it('testing a widget', async function () {
    await page.goto('http://localhost:5000/slideshow_builder')
    const data = await fetch('http://localhost:5000/api/tests', { method: 'GET' }).then(r => r.json())
    for (const widget in data) {
      const fields = data[widget]
      await selectWidget(page, widget)
      let count = 1
      for (const fieldName in fields) {
        const value = fields[fieldName]
        await fillInField(page, `span[name="${fieldName}"] textarea`, value, fields.length > count ? 'Tab' : 'Enter')
        count++
      }
      await waitForComputedFields(page)
    }
  })

  mocha.it('test the login', async function () {
    await page.goto('http://localhost:5000')
    const identifier = 'a[href="/login"]'
    await page.waitForSelector(identifier)
    await page.$eval(identifier, elem => elem.click())
    await page.waitForSelector('input[name="email"]')
    await fillInField(page, 'input[name="email"]', 'test@test.com')
    await fillInField(page, 'input[name="password"]', '12345678')
    await page.$eval('button.button.is-fullwidth', elem => elem.click())
    await page.waitForSelector('button.logout')
  })

  mocha.it('create a slideshow', async function () {
    await page.goto('http://localhost:5000')
    const identifier = 'a[href="/login"]'
    await page.waitForSelector(identifier)
    await page.$eval(identifier, elem => elem.click())
    await page.waitForSelector('input[name="email"]')
    await fillInField(page, 'input[name="email"]', 'test@test.com')
    await fillInField(page, 'input[name="password"]', '12345678')
    await page.$eval('button.button.is-fullwidth', elem => elem.click())

  })
})
