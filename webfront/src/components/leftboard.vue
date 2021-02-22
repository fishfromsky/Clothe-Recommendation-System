<template>
    <div class="container">
        <div class="title-box">
            <div>服装搭配区域</div>
            <el-button size="small" type="danger" style="margin-right: 60px" @click="submitItem">提交搭配</el-button>
        </div>
        <div class="top-box">
            <div class="top-child">
                <div class="select-box">
                    <div class="title-header">
                        <i class="el-icon-star-on" style="margin-left: 20px; color: #4ab7bd"></i>
                        <div class="top-title">上衣</div>
                    </div>
                    <div class="btn-box">
                        <el-button type="primary" @click="chooseTop">点击选择</el-button>
                    </div>
                </div>
                <div class="divider"></div>
                <div class="img-preview">
                    <div class="img-title-container">
                        <div class="img-title-text">服装预览(点击图片可放大)</div>
                    </div>
                    <div class="img-preview-container">
                        <el-image :src="choose_pic.top.src" :preview-src-list="[choose_pic.top.src]" style="width: 60%; height: 90%">
                            <div slot="error" style="width: 100%;
                                                    height: 100%;
                                                    display: flex;
                                                    flex-direction: column;
                                                    justify-content: center;
                                                    align-items: center;
                                                    background: #f5f7fa;
                                                    font-size: 30px">
                                <i class="el-icon-picture-outline" style="color:#909399"></i>
                                <div style="font-size: 13px; color: #909399">未选择服装</div>
                            </div>
                        </el-image>
                    </div>
                </div>
            </div>
        </div>
        <div class="top-box">
            <div class="top-child">
                <div class="select-box">
                    <div class="title-header">
                        <i class="el-icon-star-on" style="margin-left: 20px; color: #4ab7bd"></i>
                        <div class="top-title">下装</div>
                    </div>
                    <div class="btn-box">
                        <el-button type="primary" @click="chooseBottom">点击选择</el-button>
                    </div>
                </div>
                <div class="divider"></div>
                <div class="img-preview">
                    <div class="img-title-container">
                        <div class="img-title-text">服装预览(点击图片可放大)</div>
                    </div>
                    <div class="img-preview-container">
                        <el-image :src="choose_pic.bottom.src" :preview-src-list="[choose_pic.bottom.src]" style="width: 60%; height: 90%">
                            <div slot="error" style="width: 100%;
                                                    height: 100%;
                                                    display: flex;
                                                    flex-direction: column;
                                                    justify-content: center;
                                                    align-items: center;
                                                    background: #f5f7fa;
                                                    font-size: 30px">
                                <i class="el-icon-picture-outline" style="color:#909399"></i>
                                <div style="font-size: 13px; color: #909399">未选择服装</div>
                            </div>
                        </el-image>
                    </div>
                </div>
            </div>
        </div>
        <div class="top-box">
            <div class="top-child">
                <div class="select-box">
                    <div class="title-header">
                        <i class="el-icon-star-on" style="margin-left: 20px; color: #4ab7bd"></i>
                        <div class="top-title">鞋子</div>
                    </div>
                    <div class="btn-box">
                        <el-button type="primary" @click="chooseShoe">点击选择</el-button>
                    </div>
                </div>
                <div class="divider"></div>
                <div class="img-preview">
                    <div class="img-title-container">
                        <div class="img-title-text">服装预览(点击图片可放大)</div>
                    </div>
                    <div class="img-preview-container">
                        <el-image :src="choose_pic.shoe.src" :preview-src-list="[choose_pic.shoe.src]" style="width: 60%; height: 90%">
                            <div slot="error" style="width: 100%;
                                                    height: 100%;
                                                    display: flex;
                                                    flex-direction: column;
                                                    justify-content: center;
                                                    align-items: center;
                                                    background: #f5f7fa;
                                                    font-size: 30px">
                                <i class="el-icon-picture-outline" style="color:#909399"></i>
                                <div style="font-size: 13px; color: #909399">未选择服装</div>
                            </div>
                        </el-image>
                    </div>
                </div>
            </div>
        </div>
        <div class="top-box">
            <div class="top-child">
                <div class="select-box">
                    <div class="title-header">
                        <i class="el-icon-star-on" style="margin-left: 20px; color: #4ab7bd"></i>
                        <div class="top-title">首饰</div>
                    </div>
                    <div class="btn-box">
                        <el-button type="primary" @click="chooseAccessory">点击选择</el-button>
                    </div>
                </div>
                <div class="divider"></div>
                <div class="img-preview">
                    <div class="img-title-container">
                        <div class="img-title-text">服装预览(点击图片可放大)</div>
                    </div>
                    <div class="img-preview-container">
                        <el-image :src="choose_pic.accessory.src" :preview-src-list="[choose_pic.accessory.src]" style="width: 60%; height: 90%">
                            <div slot="error" style="width: 100%;
                                                    height: 100%;
                                                    display: flex;
                                                    flex-direction: column;
                                                    justify-content: center;
                                                    align-items: center;
                                                    background: #f5f7fa;
                                                    font-size: 30px">
                                <i class="el-icon-picture-outline" style="color:#909399"></i>
                                <div style="font-size: 13px; color: #909399">未选择服装</div>
                            </div>
                        </el-image>
                    </div>
                </div>
            </div>
        </div>
        <div class="top-box">
            <div class="top-child">
                <div class="select-box">
                    <div class="title-header">
                        <i class="el-icon-star-on" style="margin-left: 20px; color: #4ab7bd"></i>
                        <div class="top-title">拎包</div>
                    </div>
                    <div class="btn-box">
                        <el-button type="primary" @click="chooseBag">点击选择</el-button>
                    </div>
                </div>
                <div class="divider"></div>
                <div class="img-preview">
                    <div class="img-title-container">
                        <div class="img-title-text">服装预览(点击图片可放大)</div>
                    </div>
                    <div class="img-preview-container">
                        <el-image :src="choose_pic.bag.src" :preview-src-list="[choose_pic.bag.src]" style="width: 60%; height: 90%">
                            <div slot="error" style="width: 100%;
                                                    height: 100%;
                                                    display: flex;
                                                    flex-direction: column;
                                                    justify-content: center;
                                                    align-items: center;
                                                    background: #f5f7fa;
                                                    font-size: 30px">
                                <i class="el-icon-picture-outline" style="color:#909399"></i>
                                <div style="font-size: 13px; color: #909399">未选择服装</div>
                            </div>
                        </el-image>
                    </div>
                </div>
            </div>
        </div>
        <el-dialog :visible.sync="select_dialog" title="选择搭配">
            <div class="select-dialog-box">
                <el-scrollbar style="height: 100%">
                    <div v-for="(item,index) in pic_data" :key="index">
                        <div class="img-box" @click="ConfirmPic(index)">
                            <el-image :src="item.url" style="width: 100%; height: 100%"></el-image>
                        </div>
                    </div>
                </el-scrollbar>
            </div>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data(){
        return{
            select_dialog: false,
            pic_data: [],
            choose_type: -1,
            choose_pic:{
                top: {
                    value: '',
                    src: ''
                },
                bottom:{
                    value: '',
                    src: ''
                },
                shoe: {
                    value: '',
                    src: ''
                },
                accessory: {
                    value: '',
                    src: ''
                },
                bag: {
                    value: '',
                    src: ''
                }
            }
        }
    },
    methods: {
        submitItem:function(){
            if (this.choose_pic.top.value === '' || this.choose_pic.bottom.value === '' || this.choose_pic.shoe.value === ''
            || this.choose_pic.accessory.value === '' || this.choose_pic.bag.value === ''){
                this.$message.error('搭配尚未选择完全')
            }
            else{
                this.$emit('child-event', this.choose_pic)
            }
        },
        ConfirmPic:function(idx){
            if (this.choose_type === 0){
                this.choose_pic.top.value = this.pic_data[idx].value
                this.choose_pic.top.src = this.pic_data[idx].url
            }
            else if (this.choose_type === 1){
                this.choose_pic.bottom.value = this.pic_data[idx].value
                this.choose_pic.bottom.src = this.pic_data[idx].url
            }
            else if (this.choose_type === 2){
                this.choose_pic.shoe.value = this.pic_data[idx].value
                this.choose_pic.shoe.src = this.pic_data[idx].url
            }
            else if (this.choose_type === 3){
                this.choose_pic.accessory.value = this.pic_data[idx].value
                this.choose_pic.accessory.src = this.pic_data[idx].url
            }
            else if (this.choose_type === 4){
                this.choose_pic.bag.value = this.pic_data[idx].value
                this.choose_pic.bag.src = this.pic_data[idx].url
            }
            this.select_dialog = false
        },
        getData:function(url){
            this.$axios.get(url).then(res=>{
                let result = res.data
                if (result.code === 20000){
                    let img_data = []
                    for (let i=0; i<result.data.length; i++){
                        let dict = {}
                        dict['label'] = result.data[i].label
                        dict['value'] = result.data[i].value
                        let value = result.data[i].value
                        let url = value.split('/')
                        dict['url'] = 'http://127.0.0.1:5000/get_pic/'+url[url.length-2]+'/'+url[url.length-1]
                        img_data.push(dict)
                    }
                    this.pic_data = img_data
                    this.select_dialog = true
                }
                else{
                    this.$message.error('获取数据失败')
                }
            })
        },
        chooseTop:function(){
            this.choose_type = 0
            this.getData('api/get_top')
        },
        chooseBottom:function(){
            this.choose_type = 1
            this.getData('api/get_bottom')
        },
        chooseShoe:function(){
            this.choose_type = 2
            this.getData('api/get_shoe')
        },
        chooseAccessory:function(){
            this.choose_type = 3
            this.getData('api/get_accessory')
        },
        chooseBag:function(){
            this.choose_type = 4
            this.getData('api/get_bag')
        }
    }
}
</script>

<style lang="scss" scoped>
  .container{
    width: 100%;
    min-height: 600px;
    background: #fff;
    box-shadow: 0 0 10px 10px rgba(153, 153, 153, 0.1);
    margin-bottom: 40px;
    padding-bottom: 20px;
  }
  .title-box{
    width: 100%;
    height: 60px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    color: #3a71a8;
    font-size: 20px;
    font-weight: bold;
    margin-left: 20px;
  }
  .top-box{
      width: 95%;
      margin-left: 2.5%;
      margin-top: 20px;
      height: 150px;
      border: 1px dashed #444;
      border-radius: 5px;
  }
  .top-child{
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: row;
      align-items: center;
  }
  .select-box{
      width: 40%;
      height: 100%;
  }
  .top-title{
      font-size: 18px;
      color: #4ab7bd;
      font-weight: bold;
  }
  .title-header{
      width: 100%;
      height: 30%;
      display: flex;
      flex-direction: row;
      align-items: center;
  }
  .btn-box{
      width: 100%;
      height: 70%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
  }
  .divider{
      width: 0;
      height: 80%;
      border-left: 1px solid #bbb;
  }
  .select-dialog-box{
      width: 100%;
      height: 500px;
  }
  .img-box{
      width: 20%; 
      height: 150px; 
      float: left;
      padding: 10px;
      cursor: pointer;
  }
  .img-box:hover{
      box-shadow: 0 0 10px 10px rgba(153, 153, 153, 0.3);
      transition: .2s;
  }
  /deep/ .el-scrollbar__wrap {
      overflow-x: hidden;
  }
  .img-preview{
      width: 60%;
      height: 100%;
  }
  .img-title-container{
      width: 100%;
      height: 20%;
      display: flex;
      flex-direction: row;
      align-items: center;
  }
  .img-title-text{
      font-size: 14px;
      color: #409EFF;
      margin-left: 10px
  }
  .img-preview-container{
    width: 100%;
    height: 80%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .image-slot-box{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: #f5f7fa;
  }
</style>