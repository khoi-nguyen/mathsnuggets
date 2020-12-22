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
    fetch.resetMocks()
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
  })

  it('loads the fields', () => {
    expect(Object.keys(wrapper.vm.widgetData.fields).length).toBe(2)
  })

  it('updates the payload properly', async () => {
    fetch.mockResponse(JSON.stringify({
      equation: 'x^3',
      solution: 'x'
    }))
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(fetch.mock.calls[0][0]).toEqual('/api/widgets/LinearEquation')
    wrapper.setProps({ payload: { equation: 'x^2' } })
    await flushPromises()
    expect(wrapper.vm.payload).toEqual({ equation: 'x^3' })
    expect(fetch.mock.calls[1][0]).toEqual('/api/widgets/LinearEquation?equation=x%5E2')
    expect(fetch.mock.calls[2][0]).toEqual('/api/widgets/LinearEquation?equation=x%5E3')
    expect(fetch).toHaveBeenCalledTimes(3)
    wrapper.vm.payload.equation = 'x^3'
    await flushPromises()
    expect(fetch).toHaveBeenCalledTimes(3)
    wrapper.vm.payload.equation = 'x^2'
    await flushPromises()
    expect(fetch).toHaveBeenCalledTimes(3)
    wrapper.vm.payload.equation = 'x^4'
    await flushPromises()
    expect(fetch).toHaveBeenCalledTimes(4)
  })
})
