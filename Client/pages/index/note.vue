<template>
	<view>
		<view class="padding-sm">
			<form @submit="submitNote">
				<view class="cu-form-group">
					<view class="title">日期</view>
					<picker mode="date" :value="date" start="2020-12-01" end="2030-01-01" @change="DateChange">
						<view class="picker">
							{{date}}
						</view>
					</picker>
				</view>
				<view class="cu-form-group">
					<view class="title">时间</view>
					<picker mode="time" :value="time" start="08:01" end="20:01" @change="TimeChange">
						<view class="picker">
							{{time}}
						</view>
					</picker>
				</view>
				<view class="cu-form-group">
					<view class="title">内容</view>
					<input placeholder="提醒事项" name="content"></input>
					<text class='cuIcon-locationfill text-orange'></text>
				</view>
				<view class="justify-center margin">
					<view class="text-center">
						<button class="cu-btn line-green text-green" @tap="hideNote">关闭</button>
						<button form-type="submit" class="cu-btn bg-green margin-left" >提交</button>
					</view>
				</view>
			</form>
		</view>
	</view>
</template>

<script>
	import moment from 'moment'
	import {
		API_NOTE_ADD,
	} from '../../common/api.js'
	
	export default{
		props:["note"],
		data() {
			return {
				time: moment().format('HH:mm'),
				date: moment().format('YYYY-MM-DD'),
				content: '',
			}
		},
		watch: {
			
		},
		methods: {
			submitNote(e) {
				let value = e.detail.value
				let time = moment(this.date+' '+ this.time).unix()
				console.log(1122, time, this.note)
				uni.request({
					url: API_NOTE_ADD,
					method: 'POST',
					data: {
						time,
						openid: this.note.openid,
						comment_id: this.note.id,
						type: 1,
						content: value.content
					},
					success(res) {
						console.log(res)
						uni.showToast({
							title: res.data.message,
							icon: 'none',
							duration: 2000
						})
						this.$emit('hideNote')
					}
				})
			},
			hideNote () {
				this.$emit('hideNote')
			},
			TimeChange(e) {
				this.time = e.detail.value
			},
			DateChange(e) {
				this.date = e.detail.value
				console.log(33, e)
			},
			ContentChange(e) {
				console.log(44, e.detail.value)
				this.content = e.detail.value
			},
		}
	}
	
</script>

<style>
</style>
