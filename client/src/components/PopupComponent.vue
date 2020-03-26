<template>
  <div class="modal-bg" v-show="show">
    <div class="modal-container">
      <div class="modal-header">
        {{ title }}
      </div>
      <div class="modal-main">
        <!-- <slot></slot> -->
        <div class="modal-info" v-for="item in popupMessage" :key="item.index">
          {{item}}
        </div>
      </div>
      <div class="modal-footer">
        <button @click="submit">确认</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'modal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    },
    popupMessage: {
      type: Array,
      default () {
        return []
      }
    }
  },
  methods: {
    submit () {
      this.$emit('submit')
    }
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped lang="less" rel="stylesheet/less">

@import '../assets/css/style.less';

.modal-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,.5);
  z-index: 10;
}

.modal-container {
  background: #FFFFFF;
  border-radius: 10px;
  overflow: hidden;
  position: fixed;
  top: 50%;
  left: 50%;
  width: @index-title-width * 3;
  transform: translate(-50%,-50%);
}

.modal-header {
  height: @popup-header-footer-height;
  background: #409EFF;
  color: @app-text-color;
  font-size: @app-value-text-size;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: move;
}
.modal-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  height: @popup-header-footer-height;
  border-top: 1px solid #ddd;
}
.modal-footer button {
  width: 160px;
  height: 60px;
  font-size: 30px;
  border-radius: 10px;
}

.modal-main {
  padding: 20px 20px;
  width: 100%;
  color: @app-bg-color;
  font-size: @app-small-text-size;
}
</style>
