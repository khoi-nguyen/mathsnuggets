import AsyncComputed from 'vue-async-computed'
import Widget from './Widget.vue'
import flushPromises from 'flush-promises'
import { createLocalVue, shallowMount } from '@vue/test-utils'
import { enableFetchMocks } from 'jest-fetch-mock'

enableFetchMocks()

const localVue = createLocalVue()
localVue.use(AsyncComputed)

let wrapper

describe('FormField', () => {
  beforeEach(async () => {
    fetch.mockResponse(JSON.stringify([
      {
        name: 'equation',
        required: true,
        type: 'Equation'
      },
      {
        computed: true,
        name: 'solution',
        type: 'Expression'
      }
    ]))
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
    expect(wrapper.vm.fields.length).toBe(2)
  })

  it('updates the payload properly', async () => {
    fetch.mockResponse(JSON.stringify({
      equation: { value: 'x^3' },
      solution: {
        computed: true,
        value: 'x'
      }
    }))
    const field = wrapper.find('form-field-stub[name="equation"]')
    await field.vm.$emit('update:value', 'x^2')
    expect(wrapper.emitted()['update:payload'][0]).toEqual([{ equation: 'x^2' }])
    wrapper.vm.payload = { equation: 'x^2' }
    await flushPromises()
    expect(wrapper.emitted()['update:payload'][1]).toEqual([{ equation: 'x^3' }])
    expect(wrapper.emitted()['update:payload'].length).toBe(2)
  })
})
