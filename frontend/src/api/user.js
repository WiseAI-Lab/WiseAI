import request from '@/utils/request'
import { TokenApi, UserInfoApi } from '../utils/urls'

export function login(data) {
  // return this.$http.post(TokenApi, { data: data })
  return request({
    url: TokenApi,
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: UserInfoApi,
    method: 'post'
  })
}
