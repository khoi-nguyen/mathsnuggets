import 'regenerator-runtime/runtime'
import FormField from './FormField.vue'
import flushPromises from 'flush-promises'
import { createLocalVue, shallowMount } from '@vue/test-utils'
import { enableFetchMocks } from 'jest-fetch-mock'
import AsyncComputed from 'vue-async-computed'

enableFetchMocks()

const localVue = createLocalVue()
localVue.use(AsyncComputed)

let wrapper = shallowMount(FormField)

describe('FormField', () => {
  beforeEach(() => {
    wrapper = shallowMount(FormField)
    fetch.resetMocks()
  })

  it('is called', () => {
    expect(wrapper).toBeTruthy()
  })

  it('expression field without default value', async () => {
    fetch.mockResponses(JSON.stringify({
      latex: '\\frac {1}{x}',
      valid: true,
      value: '1/x'
    }))
    wrapper = shallowMount(FormField, {
      localVue,
      propsData: {
        label: 'Field',
        type: 'Expression'
      }
    })

    expect(wrapper.find('textarea')).toBeTruthy()
    expect(wrapper.html()).toContain('Field')

    wrapper.vm.value = '1/x'
    await flushPromises()
    expect(wrapper.contains('textarea')).toBeFalsy()
    expect(wrapper.html()).toContain('katex')
    expect(fetch).toHaveBeenCalledTimes(1)
  })
})
