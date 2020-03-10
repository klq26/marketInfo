<template>
  <div class="panel" @click="shouldShow">
    <p class="title">{{title}}</p>
    <p class="status" :class="isOpenning ? 'enable-color' : 'disable-color'">{{isOpenning ? '开盘' : '收盘'}}</p>
  </div>
</template>

<script>
export default {
  props: [
    'title',
    'isOpenning'
  ],
  methods: {
    shouldShow () {
      this.$emit('shouldShow')
    }
  }
}
</script>

<style scoped lang="less" rel="stylesheet/less">

@import '../assets/css/style.less';

.panel {
  display:inline-flex;
  width:100%;
  background-color: @index-title-bg-color;
}

.title {
  margin: 0px;
  padding: 0px;
  width: 100%;
  height: 60px;
  font-size: @app-title-text-size;
  text-align: left;
  color: @index-title-text-color;
  display: inline-flex;
}

.status {
  margin: 0px;
  padding: 0px;
  width: @app-title-text-size * 3;
  text-align: center;
  font-size: @app-title-text-size;
  color: @index-title-text-color;
}

.enable-color {
  color: @app-enable-color;
}

.disable-color {
  color: @app-disable-color;
}

</style>
