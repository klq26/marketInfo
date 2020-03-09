<template>
  <div @click="shouldShow">
    <p>{{title}}</p>
  </div>
</template>

<script>
  export default {
    props: [
      'title'
    ],
    // data() {
    //   return {
    //     title: '标题'
    //   }
    // },
    methods: {
      shouldShow () {
        this.$emit('shouldShow')
      }
    }
  }
</script>

<style scoped lang="less" rel="stylesheet/less">

@import '../assets/css/style.less';

p {
  margin: @index-cell-margin;
  padding: 0px 0px;
  width: 100%;
  height: 60px;
  font-size: @app-title-text-size;
  text-align: left;
  color: @index-title-text-color;
  background-color: @index-title-bg-color;
}

</style>
