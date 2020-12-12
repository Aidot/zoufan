<template>
	<view class="page">
		<!-- 		<view class="cu-bar bg-white margin-top solid-bottom">
			<view class="action">
				<text class="cuIcon-title text-orange"></text> 平分
			</view>
		</view> -->
		<scroll-view scroll-x class="bg-white nav">
			<view class="flex text-center">
				<view class="cu-item flex-sub" :class="index==TabCur?'text-red cur':''" v-for="(item, index) in labels" :key="index"
				 @tap="tabSelect" :data-id="index">
					{{item}}
				</view>
				<view class="cu-item flex-sub" :key="5" :data-id="5">
					<text class="cuIcon-moreandroid margin-lr-xs"></text>
				</view>
			</view>
		</scroll-view>
		<view class="cu-card dynamic">
			<view class="cu-item shadow" v-for="c in comments" :key="c.id">
				<view class="cu-list menu-avatar">
					<view class="cu-item">
						<view @click="visitWeibo(c.user.id)" class="cu-avatar round lg" :style="'background-image:url('+c.user.avatar+');'">
						</view>
						<view class="content flex-sub">
							<view>
								<text v-if="c.user.gender" class="margin-right-sm" :class="c.user.gender == 'f' ? 'text-pink cuIcon-female' : 'text-blue cuIcon-male'">
								</text>
								<text>{{c.user.name || c.user.id}}</text>
							</view>
							<view class="text-gray text-sm flex justify-between">
								{{c.created_at | formateDateTime}}
							</view>
						</view>
						<view>
							<view class="flex p-xs text-center">
								<view class="flex-sub padding-sm text-xl">
									<text class="cuIcon-wefill text-green" title="告警"></text>
									<view class="text-xs text-gray">扩散</view>
								</view>
							</view>
						</view>
					</view>
				</view>
				<view class="grid flex-sub padding-lr margin-top-sm">
					<text class="cu-tag sm radius" :class="c.label | labelBgcolor">{{c.label}}</text>
					<text class="cu-tag sm bg-cyan radius">{{c.label_score | formatScore}}</text>
				</view>
				<view class="text-content margin-top-sm">
					{{c.text}}
				</view>
				<view v-if="c.comments && c.comments.length > 1" class="padding-lr radius">
					<view v-for="(cc, i) in c.comments" :key="i" class="margin-top-sm">
						<view v-if="cc.id != c.id">
							<view class="text-grey text-xs margin-bottom-sm">
								<text class="cuIcon-time"></text> {{cc.created_at | formateDateTime}}
							</view>
							<view class="text-gray">{{cc.text}} </view>
						</view>
					</view>
				</view>
				<view class="text-gray flex justify-center margin-bottom-sm">
					<!-- <text class="cuIcon-appreciate margin-lr-xs"></text> -->
					<view class="padding-sm" @click="visitWeibo(c.user.id)">
						<text class="cuIcon-weibo margin-right-xs"></text>
						<text class="text-sm">访问</text>
					</view>
					<view class="padding-sm">
						<text class="cuIcon-like margin-right-xs"></text>
						<text class="text-sm">收藏</text>
					</view>
					<view class="padding-sm">
						<text class="cuIcon-remind margin-lr-xs"></text>
						<text class="text-sm">提醒</text>
					</view>
					<view class="padding-sm text-red">
						<text class="cuIcon-notice"></text>
						<text class="text-sm">告警</text>
					</view>
				</view>
			</view>
		</view>
		<uni-load-more></uni-load-more>
	</view>
</template>

<script>
	import API_HOST from '../../common/api.js'	
	import moment from 'moment'
	import 'moment/locale/zh-cn'
	const labels = ['最新', '陪伴', '认知', '安慰', '鼓励']


	export default {
		components: {
			// uniRefresh,
			// uniLoadMore,
		},
		data() {
			return {
				labels,
				title: 'Hello',
				page: 1,
				label: 0,
				comments: [],
				TabCur: 0,
			}
		},
		onLoad() {
			this.getComments()
		},
		filters: {
			formatScore(score) {
				return (score * 100).toFixed(0) + '%'
			},
			formateDateTime(s) {
				return moment(s).startOf('hour').fromNow()
			},
			formateDateT(s) {
				return moment(s).format('YYYY-MM-DD HH:mm:ss')
			},
			labelBgcolor(label) {
				let output = 'bg-red'
				switch (label) {
					case '认知':
						output = 'bg-blue'
						break
					case '安慰':
						output = 'bg-yellow'
						break
					case '鼓励':
						output = 'bg-green'
						break
					default:
						output = 'bg-orange'
				}
				return output
			}
		},
		methods: {
			visitWeibo(uid) {
				window.open('https://m.weibo.cn/u/' + uid)
			},
			tabSelect(e) {
				this.TabCur = e.currentTarget.dataset.id;
				this.label = parseInt(this.TabCur)
				console.log(this.label)
				this.comments = []
				this.page = 1
				if (this.TabCur < 5) {
					this.getComments()
				} 
				
			},
			getComments() {
				let that = this
				let {
					page,
					label
				} = this
				uni.request({
					url: API_HOST + '/a/api/items/read.php',
					data: {
						page: page,
						size: 20,
						label: label
					},
					success(res) {
						if (res.statusCode === 200) {
							let {
								meta,
								list
							} = res.data
							that.comments = that.comments.concat(list)
							if (list.length == 20) {
								that.page = page + 1
							}
						}

					}
				})
			},

			onPullDownRefresh() {
				console.log('下拉刷新', this.page);
				this.page = 1
				this.getComments()
			},
			onReachBottom(e) {
				console.log('触底加载更多', this.page)
				this.getComments()
			},
		}
	}
</script>

<style>
	.page {
		height: 100Vh;
		width: 100vw;
	}

	.page.show {
		overflow: hidden;
	}

	.qiun-charts {
		width: 750upx;
		height: 500upx;
		background-color: #FFFFFF;
	}

	.charts {
		width: 750upx;
		height: 500upx;
		background-color: #FFFFFF;
	}
</style>
