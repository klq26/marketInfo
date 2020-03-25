<template>
  <div class="container">
    <p class="title" @click="shouldShow">{{title}}</p>
    <div class="panel">
      <div class="button" @click="changeSortType" v-show="showSortButton === '1' ? true : false">{{sortNameConverter(sortType)}}</div>
      <div class="button" @click="changeShowType" v-show="showStyleButton === '1' ? true : false">样式</div>
      <p class="status" :class="isOpenning ? 'enable-color' : 'disable-color'">{{isOpenning ? '开盘' : '收盘'}}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    'title',
    'isOpenning',
    'showSortButton',
    'showStyleButton',
    'sortType'
  ],
  data () {
    return {
      sortName: '产值',
    }
  },
  methods: {
    sortNameConverter (sortType) {
      if (sortType === '1') {
        return '产值'
      }
      if (sortType === '2') {
        return '时区'
      }
      if (sortType === '3') {
        return '人均'
      }
      if (sortType === '4') {
        return '人口'
      }
      if (sortType === '5') {
        return '国土'
      }
    },
    shouldShow () {
      // // 子组件
      // this.$emit('test',this.param1，this.param2, this.param3)
      // // 父组件 arguments 是以数组的形式传入
      // @test='test(arguments,userDefined)'
      this.$emit('shouldShow')
    },
    changeShowType () {
      this.$emit('changeShowType', this.title)
    },
    changeSortType () {
      this.$emit('changeSortType', this.title, this.sortType)
    }
  }
}
</script>

<style scoped lang="less" rel="stylesheet/less">

@import '../assets/css/style.less';

.container {
  width:100%;
  background-color: @index-title-bg-color;
  display:inline-flex;
  justify-content:space-between;
}

.title {
  margin: 0px 4px;
  padding: 0px;
  width: 30%;
  height: 60px;
  font-size: @app-title-text-size;
  text-align: left;
  color: @index-title-text-color;
  display: inline-flex;
}

.panel {
  width:70%;
  background-color: @index-title-bg-color;
  display:inline-flex;
  justify-content: flex-end;
}

.button {
  margin: 0px;
  padding: 0px;
  width: @app-title-text-size * 3;
  text-align: center;
  font-size: @app-small-text-size;
  color: @index-title-text-color;
}

.status {
  margin: 0px;
  padding: 0px;
  width: @app-title-text-size * 3;
  text-align: center;
  font-size: @app-small-text-size;
  color: @index-title-text-color;
}

.enable-color {
  color: @app-enable-color;
}

.disable-color {
  color: @app-disable-color;
}

</style>
