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

async function fillInField (page, identifier, value) {
  await page.waitFor(identifier)
  const tagName = await page.$eval(identifier, el => el.tagName)
  if (tagName === 'select') {
    await page.select(identifier, value)
  } else {
    await page.focus(identifier)
    await page.keyboard.type(value)
    const typedValue = await page.$eval(identifier, el => el.value)
    assert.equal(typedValue, value)
  }
  await page.keyboard.press('Tab')
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

async function clickElement (page, identifier) {
  await page.waitForSelector(identifier)
  await page.$eval(identifier, elem => elem.click())
}

async function login (page) {
  await page.goto('http://localhost:5000')
  await clickElement(page, 'a[href="/login"]')
  await fillInField(page, 'input[name="email"]', 'test@test.com')
  await fillInField(page, 'input[name="password"]', '12345678')
  await clickElement(page, 'button.button.is-fullwidth')
}

mocha.describe('mathsnuggets', function () {
  let browser
  let page
  this.timeout(100000)

  mocha.before(async function () {
    browser = await puppeteer.launch({ headless: false, args: ['--no-sandbox'] })
    page = await browser.newPage()
    fetch('http://localhost:5000/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'test@test.com', password: '12345678' })
    })
  })

  mocha.after(async function () {
    fetch('http://localhost:5000/api/tests/user', { method: 'DELETE' })
    browser.close()
  })

  mocha.it('changing the title', async function () {
    await page.goto('http://localhost:5000/slideshow_builder')
    const identifier = 'section.present .slide-title'

    const checkTitle = async function (assertMethod, string) {
      const title = await page.$eval(identifier, el => el.innerText)
      assert[assertMethod](title, string)
    }

    await page.waitFor(identifier)
    await page.keyboard.press('Tab')
    await page.keyboard.type('Test')
    await page.keyboard.press('Enter')
    await checkTitle('equal', 'Test')

    await page.click(identifier, { clickCount: 3 })
    await page.keyboard.type('Hello')
    await page.keyboard.press('Enter')
    await checkTitle('equal', 'Hello')

    await page.keyboard.press('ArrowRight')
    await checkTitle('notEqual', 'Hello')
    await page.keyboard.press('ArrowLeft')
    await checkTitle('equal', 'Hello')
  })

  mocha.it('testing widgets', async function () {
    await page.goto('http://localhost:5000/slideshow_builder')
    const data = await fetch('http://localhost:5000/api/tests', { method: 'GET' }).then(r => r.json())
    for (const widget in data) {
      const slideTitle = await page.$('.present .box .title')
      const date = await page.$('.present .box .date')
      await slideTitle.click({ button: 'right' })
      const fields = data[widget]
      await selectWidget(page, widget)
      await date.click({ button: 'left' })
      for (const fieldName in fields) {
        const value = fields[fieldName]
        await fillInField(page, `span[name="${fieldName}"] textarea, span[name="${fieldName}"] select`, value)
      }
      await waitForComputedFields(page)
    }
  })

  mocha.xit('test the login', async function () {
    await login(page)
    await clickElement(page, 'button.logout')
  })

  mocha.xit('create a slideshow', async function () {
    await login(page)
    await clickElement(page, 'a[href="/resources"]')
    await clickElement(page, '.panel-block button.is-primary')
    await fillInField(page, '.modal input[name="title"]', 'New Slideshow')
    await clickElement(page, '.modal .is-success')
    await clickElement(page, 'a[href="/resources/new-slideshow"]')
    await page.goto('http://localhost:5000/resources')
  })
})
