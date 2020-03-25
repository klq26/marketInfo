<template>
    <div class="modal-bg" v-show="show">
        <div class="modal-container">
            <div class="modal-header">
                {{ title }}
            </div>
            <div class="modal-main">
                <!-- <slot></slot> -->
                <div v-for="item in popupMessage" :key="item.index">
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
        submit() {
            this.$emit('submit')
        },
    }
}
</script>

<style scoped lang="less" rel="stylesheet/less">

@import '../assets/css/style.less';

.modal-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 890px;
    height: 100%;
    background: rgba(0,0,0,.5);
    z-index: 10;
}
.modal-container {
    background: #fff;
    border-radius: 10px;
    overflow: hidden;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
}
.modal-header {
    height: 56px;
    background: #409EFF;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: move;
}
.modal-footer {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 57px;
    border-top: 1px solid #ddd;
}
.modal-footer button {
    width: 100px;
}
.modal-main {
    padding: 15px 40px;
}
</style>