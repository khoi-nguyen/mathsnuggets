import { shallowMount } from '@vue/test-utils'
import FormField from './FormField.vue'

let wrapper = shallowMount(FormField)

describe('FormField', () => {
  beforeEach(() => {
    wrapper = shallowMount(FormField)
  })

  it('is called', () => {
    expect(wrapper).toBeTruthy()
  })
})
