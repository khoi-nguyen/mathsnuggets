import AsyncComputed from 'vue-async-computed'
import Widget from './Widget.vue'
import flushPromises from 'flush-promises'
import { createLocalVue, shallowMount } from '@vue/test-utils'
import { enableFetchMocks } from 'jest-fetch-mock'

enableFetchMocks()

const localVue = createLocalVue()
localVue.use(AsyncComputed)

let wrapper

describe('Widget', () => {
  beforeEach(async () => {
    fetch.mockResponse(JSON.stringify({
      fields: {
        equation: {
          name: 'equation',
          required: true,
          type: 'Equation'
        },
        solution: {
          computed: true,
          name: 'solution',
          type: 'Expression'
        }
      },
      template: ''
    }))
    wrapper = shallowMount(Widget, {
      localVue,
      propsData: {
        payload: {},
        type: 'LinearEquation'
      }
    })
    await flushPromises()
    fetch.resetMocks()
  })

  it('loads the fields', () => {
    expect(Object.keys(wrapper.vm.widgetData.fields).length).toBe(2)
  })

  it('updates the payload properly', async () => {
    fetch.mockResponse(JSON.stringify({
      equation: 'x^3',
      solution: 'x'
    }))
    wrapper.setProps({ payload: { equation: 'x^2' } })
    await flushPromises()
    expect(wrapper.vm.payload).toEqual({ equation: 'x^3' })
  })
})
