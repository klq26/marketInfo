<template>
  <div id="app">
    <!-- <router-view/> -->
    <br/>
    <IndexComponent :indexInfos="china" :showType="1"/>
    <br/>
    <IndexComponent :indexInfos="asian" :showType="0"/>
    <br/>
    <IndexComponent :indexInfos="euro" :showType="1"/>
    <br/>
    <IndexComponent :indexInfos="america" :showType="0"/>
    <br/>
    <IndexComponent :indexInfos="goods" :showType="1"/>
    <br/>
    <IndexComponent :indexInfos="exchanges" :showType="0"/>
    <br/>
    <IndexComponent :indexInfos="bond" :showType="1"/>
  </div>
</template>

<script>

import axios from 'axios'
import Vue from 'vue'
// 指数组件
import IndexComponent from './components/IndexComponent'

Vue.prototype.$axios = axios
Vue.config.productionTip = false

export default {
  name: 'App',
  components: {
    IndexComponent
  },
  props : [
    'china',
    'asian',
    'euro',
    'america',
    'goods',
    'exchanges',
    'bond'
  ],
  created: function() {
    var that = this
    // 请求中国
    this.$axios.get('http://112.125.25.230/api/indexs/china').then(function (response) {
      that.china = response.data.data
    });
    // 请求亚洲
    this.$axios.get('http://112.125.25.230/api/indexs/asian').then(function (response) {
      that.asian = response.data.data
    });
    // 请求欧洲
    this.$axios.get('http://112.125.25.230/api/indexs/euro').then(function (response) {
      that.euro = response.data.data
    });
    // 请求美洲
    this.$axios.get('http://112.125.25.230/api/indexs/america').then(function (response) {
      that.america = response.data.data
    });
    // 请求期货&外汇
    this.$axios.get('http://112.125.25.230/api/goods_and_exchanges').then(function (response) {
      that.goods = response.data.data.goods
      that.exchanges = response.data.data.exchanges
    });
    // 债券&组合
    this.$axios.get('http://112.125.25.230/api/bondinfo').then(function (response) {
      that.bond = []
      for(var item in response.data.data[0].value) {
        that.bond.push(response.data.data[0].value[item])
      }
      for(var item in response.data.data[1].value) {
        that.bond.push(response.data.data[1].value[item])
      }
      for(var item in response.data.data[2].value) {
        that.bond.push(response.data.data[2].value[item])
      }
    });
  }

}
</script>

<style lang="less" rel="stylesheet/less">

@import './assets/css/style.less';

#app {
  width: 856px; /* 240 + 4 * 4 + 200 * 3 = 856 */
  background-color: @app-bg-color;
}
</style>
