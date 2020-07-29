import AsyncComputed from 'vue-async-computed'
import Buefy from 'buefy'
import FormField from './FormField.vue'
import flushPromises from 'flush-promises'
import { createLocalVue, shallowMount } from '@vue/test-utils'
import { enableFetchMocks } from 'jest-fetch-mock'

enableFetchMocks()

const localVue = createLocalVue()
localVue.use(AsyncComputed)
localVue.use(Buefy)

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

  it('markdown fields', async () => {
    fetch.mockResponses(JSON.stringify({
      html: '<strong>hello</strong>',
      valid: true,
      value: '**hello**'
    }))
    wrapper = shallowMount(FormField, {
      localVue,
      propsData: {
        label: 'Field',
        type: 'Markdown'
      }
    })
    expect(wrapper.vm.cols).toBe(5)
    expect(wrapper.find('textarea').exists()).toBe(true)
    wrapper.find('textarea').setValue('Bonjour\nHello')
    expect(wrapper.vm.cols).toBe(7)
    expect(wrapper.vm.rows).toBe(2)
    wrapper.find('textarea').trigger('blur')
    expect(wrapper.emitted()['update:value']).toEqual([['Bonjour\nHello']])
    wrapper.setProps({ value: '**hello**' })
    await flushPromises()
    expect(wrapper.find('textarea').exists()).toBe(false)
    expect(wrapper.text()).toEqual('hello')
  })

  it('select field', async () => {
    fetch.mockResponses(JSON.stringify({
      valid: true,
      value: 'foo'
    }))
    wrapper = shallowMount(FormField, {
      localVue,
      propsData: {
        label: 'Field',
        type: 'Select',
        options: ['foo', 'bar']
      }
    })
    expect(wrapper.find('select').exists()).toBe(true)
    expect(wrapper.find('option').exists()).toBe(true)
    wrapper.find('select').setValue('foo')
    wrapper.find('select').trigger('blur')
    expect(wrapper.emitted()['update:value'][0]).toEqual(['foo'])
    wrapper.setProps({ value: 'foo' })
    await flushPromises()
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(wrapper.find('select').exists()).toBe(false)
    expect(wrapper.text()).toBe('foo')
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
    expect(wrapper.find('b-button-stub').exists()).toBe(false)
    wrapper.setProps({ value: 'x' })
    await flushPromises()
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(wrapper.find('b-button-stub').exists()).toBe(true)
    await wrapper.find('b-button-stub').trigger('click')
    expect(wrapper.find('b-button-stub').exists()).toBe(false)
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
