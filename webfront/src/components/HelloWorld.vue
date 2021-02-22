<template>
  <div class="main-body">
    <dashboard></dashboard>
    <div class="child-body">
      <el-row :gutter="40">
        <el-col :span="8">
          <leftboard @child-event="handleLeftChildEvent"></leftboard>
        </el-col>
        <el-col :span="16">
          <rightboard :msg-val="childMsg"></rightboard>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import dashboard from './dashboard'
import leftboard from './leftboard'
import Rightboard from './rightboard.vue'
export default {
  name: 'HelloWorld',
  components: {
    dashboard,
    leftboard,
    Rightboard
  },
  data () {
    return {
      childMsg: {}
    }
  },
  methods: {
    handleLeftChildEvent:function(val){
      this.childMsg = val
    }
  }
}
</script>

<style scoped>
  .main-body{
    position: absolute;
    width: 100%;
    min-height: 100%;
    top: 0;
    left: 0;
    background: #f0f2f5;
  }
  .child-body{
    padding-top: 20px;
    padding-left: 20px;
    padding-right: 20px;
  }
</style>
