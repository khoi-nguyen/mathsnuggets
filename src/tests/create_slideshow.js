const assert = require('assert')
const mocha = require('mocha')
const puppeteer = require('puppeteer')

async function selectWidget (page, widget) {
  await page.hover('.widget-col')
  await page.select('.widget-col select', widget)
}

async function fillInField (page, fieldName, value, key = 'Enter') {
  const identifier = `span[name="${fieldName}"] textarea`
  await page.waitFor(identifier)
  await page.focus(identifier)
  await page.keyboard.type(value)
  const typedValue = await page.$eval(identifier, el => el.value)
  assert.equal(typedValue, value)
  await page.keyboard.press(key)
}

async function checkComputedField (page, fieldName) {
  const identifier = `span[name="${fieldName}"] button`
  await page.waitFor(identifier)
  await page.click(identifier)
}

mocha.describe('mathsnuggets', function () {
  let browser
  let page

  mocha.before(async function () {
    browser = await puppeteer.launch({ headless: false, slowMo: 100 })
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
    await selectWidget(page, 'Equation')
    await fillInField(page, 'equation', 'x^2 - 5x + 6')
    await checkComputedField(page, 'solution')
  })
})
