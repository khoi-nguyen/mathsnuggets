import ErrorMessage from './ErrorMessage.vue'
import Buefy from 'buefy'
import { createLocalVue, mount } from '@vue/test-utils'

let wrapper

const localVue = createLocalVue()
localVue.use(Buefy)

describe('ErrorMessage', () => {
  beforeEach(() => {
    wrapper = mount(ErrorMessage, {
      localVue,
      propsData: {
        message: '',
        traceback: 'foobar'
      }
    })
  })

  it('Is empty', () => {
    expect(wrapper.html()).toBe('')
  })

  it('show error and traceback', async () => {
    await wrapper.setProps({ message: 'foo' })
    expect(wrapper.html()).toContain('foo')
    expect(wrapper.html()).not.toContain('foobar')
    expect(wrapper.find('button').exists()).toBe(true)
    await wrapper.find('button').trigger('click')
    expect(wrapper.html()).toContain('foobar')
    expect(wrapper.find('button').exists()).toBe(false)
  })
})
