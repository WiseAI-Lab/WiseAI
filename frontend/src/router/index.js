import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/',
    redirect: '/index',
  }, 
  {
    path: '/index',
    component: () => import('@/views/index/index'),
    redirect: 'wise',
    children:[
      {
        path: '/wise',
        name: 'wise',
        component:() =>  import('@/views/index/wise'),
      },
      {
        path: 'agent',
        name: 'agent',
        component:() =>  import('@/views/agent/index'),
        children:[
          {
            path: 'basic_agent_list',
            name: 'basic_agent_list',
            component:() =>  import('@/views/agent/basic_agent_list'),
          },
          {
            path: 'basic_agent_info/:agent_id',
            name: 'basic_agent_info',
            component:() =>  import('@/views/agent/basic_info'),
          },
          {
            path: 'init_agent',
            name: 'init_agent',
            component:() =>  import('@/views/agent/init_agent'),
          },

        ]
      },
      {
        path: '/my_agents',
        name: 'my_agents',
        component:() =>  import('@/views/agent/my_agents'),
        children:[
          {
            path: 'card/:id', 
            name: 'my_agent_card', 
            component:() =>import('@/views/agent/my_agents'),
            props: (route) => {
              let id = parseInt(route.params.id);
              return { id };
            } 
          }
        ]
      }
    ]
  }, 
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
  }, 
]


const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
