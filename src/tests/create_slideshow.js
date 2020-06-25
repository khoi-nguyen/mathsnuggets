const assert = require('assert')
const fetch = require('node-fetch')
const mocha = require('mocha')
const puppeteer = require('puppeteer')

async function selectWidget (page, widget) {
  await page.click('.widget-search')
  const identifier = '.autocomplete input'
  await page.waitFor(identifier)
  await page.click(identifier, { clickCount: 3 })
  await page.keyboard.type(widget)
  const typedValue = await page.$eval(identifier, el => el.value)
  assert.equal(typedValue, widget)
  await page.keyboard.press('Enter')
}

async function fillInField (page, fieldName, value, key = 'Tab') {
  const identifier = `span[name="${fieldName}"] textarea`
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
}

mocha.describe('mathsnuggets', function () {
  let browser
  let page
  this.timeout(100000)

  mocha.before(async function () {
    browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] })
    page = await browser.newPage()
    await page.goto('http://localhost:5000/slideshow_builder')
  })

  mocha.after(async function () {
    browser.close()
  })

  mocha.it('changing the title', async function () {
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
    const data = await fetch('http://localhost:5000/api/tests', { method: 'GET' }).then(r => r.json())
    for (const widget in data) {
      const fields = data[widget]
      await selectWidget(page, widget)
      let count = 1
      for (const fieldName in fields) {
        const value = fields[fieldName]
        await fillInField(page, fieldName, value, fields.length > count ? 'Tab' : 'Enter')
        count++
      }
      await waitForComputedFields(page)
    }
  })
})
