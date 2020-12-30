import Vue from 'vue'
import App from './App'

// we7
import util from './common/we7_js/util.js'
import siteInfo from './common/we7_js/siteinfo.js'

import basics from './pages/basics/home.vue'
Vue.component('basics',basics)

import components from './pages/component/home.vue'
Vue.component('components',components)

import plugin from './pages/plugin/home.vue'
Vue.component('plugin',plugin)

import cuCustom from './colorui/components/cu-custom.vue'
Vue.component('cu-custom',cuCustom)

Vue.config.productionTip = false

App.mpType = 'app'
App.util = util
App.siteInfo = siteInfo

const app = new Vue({
    ...App
})
app.$mount()

 



