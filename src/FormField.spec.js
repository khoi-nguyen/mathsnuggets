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

    expect(wrapper.find('textarea').exists()).toBe(true)
    expect(wrapper.html()).toContain('Field')
    wrapper.find('textarea').setValue('1/x')
    wrapper.find('textarea').trigger('blur')
    expect(wrapper.emitted()['update:value']).toEqual([['1/x']])
    wrapper.setProps({ value: '1/x' })
    await flushPromises()
    expect(wrapper.find('error-message-stub').exists()).toBe(false)
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(wrapper.find('textarea').exists()).toBe(false)
    expect(wrapper.html()).toContain('katex')
    await wrapper.find('.field').trigger('click')
    expect(wrapper.find('textarea').exists()).toBe(true)
  })

  it('computed field', async () => {
    fetch.mockResponses(JSON.stringify({
      latex: '\\frac {1}{x}',
      valid: true,
      value: '1/x'
    }))
    wrapper = shallowMount(FormField, {
      localVue,
      propsData: {
        computed: true,
        label: 'Field',
        type: 'Expression'
      }
    })
    expect(wrapper.find('b-button').exists()).toBe(false)
    wrapper.setProps({ value: 'x' })
    await flushPromises()
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(wrapper.find('b-button').exists()).toBe(true)
    await wrapper.find('b-button').trigger('click')
    expect(wrapper.find('b-button').exists()).toBe(false)
    expect(wrapper.find('.katex').exists()).toBe(true)
  })

  it('validation error', async () => {
    fetch.once(JSON.stringify({
      error: true,
      message: 'foobar'
    }))
    fetch.once(JSON.stringify({
      latex: '\\frac {1}{x}',
      valid: true,
      value: '1/x'
    }))
    wrapper = shallowMount(FormField, {
      localVue,
      propsData: {
        label: 'Field',
        type: 'Expression',
        value: '1/'
      }
    })
    await flushPromises()
    expect(wrapper.find('error-message-stub').exists()).toBe(true)
    wrapper.setProps({ value: 'x' })
    await flushPromises()
    expect(wrapper.find('error-message-stub').exists()).toBe(false)
  })
})
