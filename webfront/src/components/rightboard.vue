<template>
    <div class="container">
      <div class="title-box">
        <div class="title-text">评估结果及系统建议</div>
        <el-button size="small" type="danger" style="margin-right: 60px" @click="startEvaluate">开始评估</el-button>
      </div>
      <div class="option-box">
        <div class="option-title">
          <i class="el-icon-s-opportunity" style="color: #4ab7bd; margin-left: 10px"></i>
          <div class="option-title-text">原始服装搭配</div>
        </div>
        <div class="clothe-box">
          <div v-if="hasClothe" class="clothe-box-container">
            <div class="pic-card fade1">
              <img :src="clothe_data.top.src" style="width: 100%; height: 100%; border-radius: 10px">
            </div>
            <div class="pic-card">
              <img :src="clothe_data.bottom.src" style="width: 100%; height: 100%; border-radius: 10px">
            </div>
            <div class="pic-card">
              <img :src="clothe_data.shoe.src" style="width: 100%; height: 100%; border-radius: 10px">
            </div>
            <div class="pic-card">
              <img :src="clothe_data.accessory.src" style="width: 100%; height: 100%; border-radius: 10px">
            </div>
            <div class="pic-card">
              <img :src="clothe_data.bag.src" style="width: 100%; height: 100%; border-radius: 10px">
            </div>
          </div>
        </div>
        <div class="option-title">
          <i class="el-icon-s-opportunity" style="color: #4ab7bd; margin-left: 10px"></i>
          <div class="option-title-text">系统评估结果及推荐方案</div>
        </div>
        <div class="clothe-box" v-loading="loading_status" element-loading-text="正在努力评估中,请耐心等待..."
         element-loading-background="rgba(0, 0, 0, 0.8)">
         <div v-if="hasNewClothe" class="clothe-box-container">
            <div class="pic-card fade1">
              <img :src="new_clothe_data.top.src" style="width: 100%; height: 100%; border-radius: 10px">
            </div>
            <div class="pic-card">
              <img :src="new_clothe_data.bottom.src" style="width: 100%; height: 100%; border-radius: 10px">
            </div>
            <div class="pic-card">
              <img :src="new_clothe_data.shoe.src" style="width: 100%; height: 100%; border-radius: 10px">
            </div>
            <div class="pic-card">
              <img :src="new_clothe_data.accessory.src" style="width: 100%; height: 100%; border-radius: 10px">
            </div>
            <div class="pic-card">
              <img :src="new_clothe_data.bag.src" style="width: 100%; height: 100%; border-radius: 10px">
            </div>
          </div>
        </div>
        <div class="score-box" v-if="hasNewClothe">
          <i class="el-icon-s-claim" style="color: rgb(64, 158, 255); margin-left: 40px"></i>
          <div class="score-text">原始搭配评分：</div>
          <div class="score-text1">{{score_before_update}}</div>
        </div>
        <div class="score-box" v-if="hasNewClothe" style="padding-bottom: 40px">
          <i class="el-icon-s-claim" style="color: rgb(64, 158, 255); margin-left: 40px"></i>
          <div class="score-text">系统推荐搭配评分：</div>
          <div class="score-text1">{{score_after_update}}</div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
    props:{
      msgVal: Object
    },
    data(){
      return{
        hasClothe: false,
        hasNewClothe: false,
        loading_status: false,
        clothe_data:{},
        new_clothe_data: {},
        score_before_update: -1,
        score_after_update: -1
      }
    },
    methods: { 
      isEmptyObject(obj) {
        for (var key in obj) {
          return false;
        }
        return true;
      },
      transfer_to_url:function(path){
        let url = path.split('/')
        return 'http://127.0.0.1:5000/get_pic/'+url[url.length-2]+'/'+url[url.length-1]
      },
      startEvaluate:function(){
        this.hasNewClothe = false
        if (this.isEmptyObject(this.clothe_data)){
          this.$message.error('请先提交搭配方案')
        }
        else if (this.loading_status){
          this.$message.error('已有任务在进行中，请耐心等待')
        }
        else{
          this.loading_status = true
          let post_data = {}
          post_data.top = this.clothe_data.top.value
          post_data.bottom = this.clothe_data.bottom.value
          post_data.shoe = this.clothe_data.shoe.value
          post_data.accessory = this.clothe_data.accessory.value
          post_data.bag = this.clothe_data.bag.value
          this.$axios({
            method: 'post',
            url: 'api/evaluate',
            data: post_data
          }).then(res=>{
            this.score_before_update = res.data.score
            this.score_after_update = res.data.best_score
            this.loading_status = false
            let tmp = this.clothe_data
            this.new_clothe_data = JSON.parse(JSON.stringify(tmp))
            let result = res.data.best_img_path
            if ('upper' in result){
              this.new_clothe_data.top.value = result.upper
              this.new_clothe_data.top.src = this.transfer_to_url(result.upper)
            }
            if ('bottom' in result){
              this.new_clothe_data.bottom.value = result.bottom
              this.new_clothe_data.bottom.src = this.transfer_to_url(result.bottom)
            }
            if ('shoe' in result){
              this.new_clothe_data.shoe.value = result.shoe
              this.new_clothe_data.shoe.src = this.transfer_to_url(result.shoe)
            }
            if ('accessory' in result){
              this.new_clothe_data.accessory.value = result.accessory
              this.new_clothe_data.accessory.src = this.transfer_to_url(result.accessory)
            }
            if ('bag' in result){
              this.new_clothe_data.bag.value = result.bag
              this.new_clothe_data.bag.src = this.transfer_to_url(result.bag)
            }
            console.log(this.new_clothe_data)
            this.hasNewClothe = true
          })
        }
      }
    },
    watch:{
      msgVal(val){
        this.hasClothe = true
        this.clothe_data = val
      }
    }
}
</script>

<style scoped>
  .container{
    width: 100%;
    min-height: 300px;
    background: #fff;
    box-shadow: 0 0 10px 10px rgba(153, 153, 153, 0.1);
  }
  .title-box{
    width: 100%;
    height: 60px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
  .title-text{
    font-size: 20px;
    font-weight: bold;
    color: #3a71a8;
    margin-left: 20px
  }
  .option-box{
    width: 90%;
    margin-left: 5%;
    min-height: 300px;
  }
  .option-title{
    width: 100%;
    height: 60px;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  .option-title-text{
    font-size: 15px;
    font-weight: bold;
    color: #4ab7bd;
  }
  .clothe-box{
    width: 100%;
    height: 250px;
  }
  .clothe-box-container{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-around;
  }
  .pic-card{
    width: 17%;
    height: 90%;
    box-shadow: 0 0 10px 10px rgba(153, 153, 153, 0.2);
    border-radius: 10px;
  }
  @keyframes fade-in{
    0%{
      margin-top: -15%;
      opacity: 0;
    }
    100%{
      margin-top: 0;
      opacity: 1;
    }
  }
  @-webkit-keyframes fade-in{
    0%{
      margin-top: -15%;
      opacity: 0;
    }
    100%{
      margin-top: 0;
      opacity: 1;
    }
  }
  .fade1{
    animation: fade-in;
    animation-direction: 1s;
  }
  .score-box{
    width: 100%;
    height: 80px;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  .score-text{
    font-size: 15px;
    font-weight: bold;
    color: rgb(64, 158, 255);
    margin-left: 10px;
  }
  .score-text1{
    font-size: 20px;
    font-weight: bold;
    color: #666;
    margin-left: 10px;
  }
</style>