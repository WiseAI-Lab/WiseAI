import { get_basic_agent_list, get_basic_agent_info, get_user_agent_list, get_user_agent_info} from '@/api/agent'

const state = {
  basic_agent_list: []
}

const mutations = {
  SET_BASIC_AGENT_LIST: (state, agent_list) => {
    state.basic_agent_list = agent_list
  },
}

const actions = {
  get_basic_agent_list() {
    return new Promise((resolve, reject) => {
      get_basic_agent_list().then(response => {
        const { data } = response
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  get_basic_agent_info({ commit }, agent_info) {
    const { agent_id } = agent_info
    return new Promise((resolve, reject) => {
      get_basic_agent_info({ agent_id: agent_id }).then(response => {
        const { data } = response
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  get_user_agent_list() {
    return new Promise((resolve, reject) => {
      get_user_agent_list().then(response => {
        const { data } = response
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  get_user_agent_info({ commit }, agent_info) {
    const { agent_id } = agent_info
    return new Promise((resolve, reject) => {
      get_user_agent_info({ agent_id: agent_id }).then(response => {
        const { data } = response
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
