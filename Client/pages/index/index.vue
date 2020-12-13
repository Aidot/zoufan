<template>
	<view class="page">
		<view class="cu-bar search bg-white solid-bottom">
			<view class="search-form round">
				<text class="cuIcon-search"></text>
				<input 
					@blur="searchBlur"
					@confirm="searchBlur"
					:adjust-position="false" 
					type="text"
					v-model="keyword"
					placeholder="关键词"
					confirm-type="search"></input>
			</view>
			<view class="action margin-left">
				<text @click="navFavor()" :class="showFavor?'cuIcon-likefill text-orange':'cuIcon-likefill'">
				</text>
			</view>
		</view>
	
		<!-- <text class="cuIcon-title text-orange"></text> -->
		<scroll-view scroll-x scroll-with-animatio class="bg-white nav" :scroll-left="scrollLeft">
			<view class="flex text-center">
				<view class="cu-item flex-sub" :class="index==TabCur?'text-red cur':''" v-for="(item, index) in labels" :key="index"
				 @tap="tabSelect" :data-id="index">
					{{item}}
				</view>
			</view>
		</scroll-view>
		<view class="cu-card dynamic">
			<view class="cu-item shadow" v-for="(c, i) in comments" :key="c.id">
				<view class="cu-list menu-avatar">
					<view class="cu-item padding-l-140">
						<view @click="visitWeibo(c.user.id)" class="cu-avatar round lg" :style="'background-image:url('+c.user.avatar+');'">
						</view>
						<view class="flex-sub">
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
							<view class="flex p-xs text-center" @click="sendWxMsg('group', c)">
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
					<view class="padding-sm" @click="addFavor(c.id, i)">
						<text class="cuIcon-like margin-right-xs" :class="c.favor ? 'text-red': ''"></text>
						<text class="text-sm">收藏</text>
					</view>
					<view class="padding-sm" @click="addNote(c.id)">
						<text class="cuIcon-remind margin-lr-xs"></text>
						<text class="text-sm">提醒</text>
					</view>
					<view @click="sendWxMsg('sos', c)" class="padding-sm text-red">
						<text class="cuIcon-notice"></text>
						<text class="text-sm">告警</text>
					</view>
				</view>
				<Note v-if="note.id === c.id" :note="note" @hideNote="hideNote" />
			</view>
		</view>
		<uni-load-more :contentText="loadmoreText"></uni-load-more>
	</view>
</template>

<script>
	import {
		API_COMMENTS,
		API_AUTH,
		API_FAVOR_ADD,
		API_WX_MSG
	} from '../../common/api.js'
	import moment from 'moment'
	import 'moment/locale/zh-cn'
	import Note from './note.vue'
	const labels = ['最新', '陪伴', '认知', '安慰', '鼓励']


	export default {
		components: {
			// uniRefresh,
			// uniLoadMore,
			Note,
		},
		data() {
			return {
				labels,
				title: 'Hello',
				page: 1,
				label: 0,
				keyword: '',
				comments: [],
				TabCur: 0,
				openid: '123',
				fan: 1,
				mid: 1,
				scrollLeft: 0,
				showFavor: false,
				note: {
					openid: null,
					id: null,
				},
				loadmoreText: {
					contentdown: "",
					contentrefresh: "正在加载...",
					contentnomore: "没有更多数据了"
				}
			}
		},
		onLoad() {
			this.getAuth()
			this.getComments()
		},
		filters: {
			formatScore(score) {
				return (score * 100).toFixed(0) + '%'
			},
			formateDateTime(s) {
				return moment(s).startOf('second').fromNow()
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
			navFavor() {
				this.showFavor = !this.showFavor
				this.page = 0
				this.comments = []
				this.getComments()
			},
			searchBlur() {
				this.comments = []
				this.getComments()
			},
			sendWxMsg(action, c) {
				console.log('group msg', c)
				let params = {
					action,
					id: c.id,
					openid: this.openid
				}
				uni.showModal({
				    title: '提醒',
				    content: '点击确定，消息将转发到微信群。',
				    success: function (res) {
				        if (res.confirm) {
				           uni.request({
				           	url: API_WX_MSG,
				           	method: "POST",
				           	data: params,
				           	success(res) {
				           		uni.showToast({
				           			title: res.data.message,
				           			icon: 'none',
				           			duration: 2000
				           		});
				           	}
				           }) 
				        }
				    }
				});
			},
			tabSelect(e) {
				this.showFavor = false
				this.TabCur = e.currentTarget.dataset.id;
				this.label = parseInt(this.TabCur)
				this.scrollLeft = (e.currentTarget.dataset.id - 1) * 100
				console.log(this.label)
				this.keyword = ''
				this.comments = []
				this.page = 1
				if (this.TabCur < 5) {
					this.getComments()
				}

			},
			getAuth() {
				uni.request({
					url: API_AUTH,
					success(res) {
						this.openid = res.data.openid
						this.mid = res.data.mid
						this.fan = res.data.fan
					}
				})
			},
			getComments() {
				uni.showLoading({  
				    title: '加载中'  
				});
				let that = this
				let {
					openid,
					page,
					label,
					keyword,
				} = this
				uni.request({
					url: API_COMMENTS,
					data: {
						openid,
						page: page,
						size: 20,
						label: label,
						keyword,
						action: this.showFavor ? 'favtors' : null
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
						uni.hideLoading();  
					}
				})
			},
			addNote(cid) {
				// if (!this.fan) return
				let { id } = this.note
				this.note = {
					openid: this.openid,
					id: !id ? cid : null,
				}				
			},
			hideNote() {
				this.note = {
					id: null
				}
			},
			addFavor(id, i) {
				if (!this.openid) return
				let that = this
				uni.request({
					method: 'POST',
					url: API_FAVOR_ADD,
					data: {
						openid: this.openid,
						mid: this.mid,
						comment_id: id
					},
					success(res) {
						console.log(res)
						uni.showToast({
							title: res.data.message,
							icon: 'none',
							duration: 2000
						});
						that.comments[i].favor = 1
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
	.padding-l-140 {
		padding-left: 140upx;
	}
	.page.show {
		overflow: hidden;
	}

	.VerticalNav.nav {
		width: 200upx;
		white-space: initial;
	}

	.VerticalNav.nav .cu-item {
		width: 100%;
		text-align: center;
		background-color: #fff;
		margin: 0;
		border: none;
		height: 50px;
		position: relative;
	}

	.VerticalNav.nav .cu-item.cur {
		background-color: #f1f1f1;
	}

	.VerticalNav.nav .cu-item.cur::after {
		content: "";
		width: 8upx;
		height: 30upx;
		border-radius: 10upx 0 0 10upx;
		position: absolute;
		background-color: currentColor;
		top: 0;
		right: 0upx;
		bottom: 0;
		margin: auto;
	}

	.VerticalBox {
		display: flex;
	}

	.VerticalMain {
		background-color: #f1f1f1;
		flex: 1;
	}
</style>
