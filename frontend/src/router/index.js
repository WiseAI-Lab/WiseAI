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
        children: [
            {
                path: '/wise',
                name: 'wise',
                component: () => import('@/views/index/wise'),
            },
            {
                path: 'basic_agent',
                name: 'basic_agent',
                component: () => import('@/views/basic_agent/index'),
                children: [
                    {
                        path: 'list',
                        name: 'basic_agent_list',
                        component: () => import('@/views/basic_agent/list'),
                    },
                    {
                        path: 'info/:agent_id',
                        name: 'basic_agent_info',
                        component: () => import('@/views/basic_agent/info'),
                    },
                    {
                        path: 'initial',
                        name: 'initial_agent',
                        component: () => import('@/views/basic_agent/initial'),
                    },

                ]
            },
            {
                path: 'user_agent',
                name: 'user_agent',
                component: () => import('@/views/user_agent/index'),
                children: [
                    {
                        path: 'list',
                        name: 'user_agent_list',
                        component: () => import('@/views/user_agent/list'),
                    },
                    {
                        path: 'info/:agent_id',
                        name: 'user_agent_info',
                        component: () => import('@/views/user_agent/info'),
                    },
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
    scrollBehavior: () => ({y: 0}),
    routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
    const newRouter = createRouter()
    router.matcher = newRouter.matcher // reset router
}

export default router
