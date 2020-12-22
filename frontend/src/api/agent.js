import request from '@/utils/request'
import { BasicAgentListApi, BasicAgentInfoApi } from '../utils/urls'

export function get_basic_agent_list() {
  return request({
    url: BasicAgentListApi,
    method: 'get',
  })
}

export function get_basic_agent_info(data) {
  return request({
    url: BasicAgentInfoApi + '/' + data.agent_id,
    method: 'get',
  })
}
