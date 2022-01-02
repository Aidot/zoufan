<template>
	<view class="page">
		<view class="cu-bar search bg-white solid-bottom">
			<view class="search-form round">
				<text class="cuIcon-search"></text>
						<!-- @blur="searchBlur" -->
				<input 
					@confirm="searchBlur"
					:adjust-position="false" 
					type="text"
					v-model="keyword"
					placeholder="搜索超话"
					confirm-type="search"></input>
			</view>
			<view class="action margin-left">
				<text @click="navFavor()" :class="showFavor?'cuIcon-attentionfavor text-orange':'cuIcon-attentionfavor'">
				</text>
			</view>
		</view>
	
		<!-- <text class="cuIcon-title text-orange"></text> -->
		<scroll-view scroll-x scroll-with-animatio class="bg-white nav" :scroll-left="scrollLeft">
			<view class="flex text-center">
				<view class="cu-item flex-sub" :class="index==1?'text-red cur':''" v-for="(item, index) in menus" :key="index"
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
								<text selectable="true">{{c.user.name || c.user.id}}</text>
							</view>
							<view class="text-gray text-sm flex justify-between">
								{{c.created_at | formateDateTime}}
							</view>
						</view>
						<view>
							<view class="flex p-xs text-center" @click="sendWxMsg('sos', c)">
								<view class="padding-sm text-xl">
									<text class="cuIcon-notice text-red" title="告警"></text>
									<view class="text-xs text-gray">告警</view>
								</view>
							</view>
						</view>
					</view>
				</view>
	
				<view class="text-content-box margin-top-sm padding-bottom-xl">
					<text selectable="true">{{c.text}}</text>
				</view>
				
				<view class="text-grey text-sm flex justify-center margin-bottom-sm">
						<view class="padding-sm" @click="visitWeibo(c.user.id, c.id)">
							<text class="cuIcon-weibo margin-right-xs"></text>
							<text>主页</text>
						</view>
						<view class="padding-sm" @click="getHistories(c.user.name)">
							<text class="cuIcon-text margin-right-xs"></text>
							<text>记录</text>
						</view>
						<view class="padding-sm" @click="visitMblog(c.mid)">
							<text class="cuIcon-link margin-right-xs"></text>
							<text>来源</text>
						</view>
				</view>
				
			</view>
		</view>
		<uni-load-more :contentText="loadmoreText"></uni-load-more>
	</view>
</template>

<script>
	import {
		API_COMMENTS,
		API_TOPICS,
		API_AUTH,
		API_FAVOR,
		API_WX_MSG
	} from '../common/api.js'
	import moment from 'moment'
	import 'moment/locale/zh-cn'
	import VConsole from 'vconsole'
	const vConsole = new VConsole()
	
	import request from "@/common/pocky-request/index.js"
	const instance = new request()
	const menus = ['评论区', '超话']
	const labels = ['评论区', '超话']
	
	export default {
		components: {
		},
		data() {
			return {
				menus,
				labels,
				title: 'Hello',
				page: 1,
				label: 0,
				keyword: '',
				since_id: 0,
				before_id: 0,
				getAction: 'before',
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
				isLoading: false,
				loadmoreText: {
					contentdown: "",
					contentrefresh: "正在加载...",
					contentnomore: "没有更多数据了"
				},
				scrollTop: 0,
			}
		},
		onLoad() {
			this.getStorageComments()
			this.getAuth()
		},
		onPageScroll(e) {
			this.scrollTop = e.scrollTop;
		},
		onShow() {
			let that = this
			this.getStorageComments()
			uni.getStorage({
				key:"newsTop",
				success:(res)=> {
					var timer = setTimeout(()=>{
						uni.pageScrollTo({
						    scrollTop: res.data,
						    duration: 0
						});
						clearTimeout(timer);
					}, 50)
				}
			})
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
					case '评论区':
						output = 'bg-blue'
						break
					case '超话':
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
			getStorageComments() {
				let that = this
				uni.getStorage({
					key: 'comments',
					success: (res) => {
						that.comments = res.data
						that.before_id = that.comments.slice(-1)[0].mid
					},
					fail: () => {
						that.getComments()
					}
				})
			},
			visitWeibo(uid, id) {
				uni.setStorage({
					key: 'comments',
					data: this.comments,
				})
				uni.setStorage({
					key: "newsTop",
					data: this.scrollTop,
					success() {
						console.log('成功了')
					},
						fail() {
						console.log('缓存失败了')
					}
				})
				window.open('https://m.weibo.cn/u/' + uid)
			},
			visitMblog(mid) {
				uni.setStorage({
					key: 'comments',
					data: this.comments,
				})
				uni.setStorage({
					key: "newsTop",
					data: this.scrollTop,
					success() {
						console.log('成功了')
					},
						fail() {
						console.log('缓存失败了')
					}
				})
				window.open('https://m.weibo.cn/detail/' + mid)
			},
			chatWeibo(uid) {
				uni.setStorage({
					key: "newsTop",
					data:this.scrollTop,
					success() {
						console.log('成功了')
					},
						fail() {
						console.log('缓存失败了')
					}
				})
				// window.open('https://weibo.cn/qr/userinfo?uid='+uid)
			},
			navFavor() {
				this.showFavor = !this.showFavor
				this.before_id = 0
				this.page = 1
				this.comments = []
				this.getComments()
			},
			searchBlur() {
				this.before_id = 0
				this.getComments()
				uni.navigateTo({ url: '?keyword='+this.keyword});
			},
			getHistories(keyword) {
				this.before_id = 0
				this.keyword = keyword;
				this.getComments()
			},
			sendWxMsg(action, c) {
				console.log('group msg', c)
				let groupname = action == 'sos' ? '专家' : '志愿者'
				let params = {
					action,
					id: c.id,
					openid: this.openid,
					type: 'topic'
				}
				let created_at = moment(c.created_at).format('YYYY-MM-DD HH:mm:ss');
				let link = `https://m.weibo.cn/u/${c.user.id}`;
				let msg = `🔔\n${c.user.name}说：\n--- ---\n${c.text}\n--- ---\n${created_at}\n${link}`;
				//复制文本
				let top = this.scrollTop;
				uni.setClipboardData({
					data: msg,
					showToast: false,
					success: function () {
						uni.pageScrollTo({
						    scrollTop: top,
						    duration: 0
						});
						console.log('复制成功', top, this.scrollTop);
					}
				});
				uni.showModal({
				    title: '提醒',
				    content: '求助信息已复制。\n点击确定，将转发到'+groupname+'群。',
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
				this.before_id = 0
				this.scrollLeft = (e.currentTarget.dataset.id - 1) * 100
				this.keyword = ''
				this.comments = []
				this.page = 1
				// if (this.TabCur < 5) {
				// 	this.getComments()
				// }
				let to = this.TabCur == 0 ? '/pages/index/index' : '/pages/topics'
				uni.navigateTo({
					url: to
				})
			},
			getAuth() {
				// /app/index.php?i=3&c=entry&do=auth&action=getinfo&m=crm_weibo
				let that = this
				instance.request({
					data: {
						do: 'auth',
						action: 'getinfo'
					},
					method: 'post',
				}).then(res => {
					that.openid = res.data.openid
					that.mid = res.data.mid
					that.fan = res.data.fan
					console.log('[Auth]', 'openid', that.openid)
				})
			},
			getComments() {
				if (this.isLoading) {
					return
				}
				uni.showLoading({  
				    title: '加载中'  
				});
				let that = this
				let {
					openid,
					page,
					label,
					keyword,
					since_id,
					before_id,
				} = this
				
				that.isLoading = true
				uni.request({
					url: API_TOPICS,
					data: {
						openid,
						size: 20,
						label: label,
						keyword,
						page,
						before_id,
						action: this.showFavor ? 'favtors' : null
					},
					success: (res) => {
						if (res.statusCode === 200) {
							let {
								meta,
								list
							} = res.data
							if (before_id > 0) {
								that.comments = that.comments.concat(list)
							} else {
								that.comments = list
							}
							
							if (list.length > 0 ) {
								that.page = page + 1
							}
							that.since_id = list[0].mid
							that.before_id = list.slice(-1)[0].mid
						} else {
							uni.showToast({
								title: '没有了',
								icon: 'none',
								duration: 1000
							});
						}
						console.log(that.before_id)
						that.isLoading = false
						uni.hideLoading();
						uni.stopPullDownRefresh()
					},
					fail: (fail) => {
						console.log(fail)
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
				let isFavor = this.comments[i].favor
				let {openid, mid} = this
				let that = this
				console.log('[Favor]', isFavor, openid)
				uni.request({
					method: 'POST',
					url: API_FAVOR,
					data: {
						openid,
						mid,
						comment_id: id,
						action: isFavor ? 'cancel' : 'add'
					},
					success(res) {
						uni.showToast({
							title: res.data.message,
							icon: 'none',
							duration: 2000
						});
						that.comments[i].favor = !isFavor
					}
				})
			},
			onPullDownRefresh() {
				console.log('下拉刷新');
				this.page = 1
				this.before_id = 0
				uni.removeStorage({
					key: 'comments',
					success: () => {
						this.comments = []
						this.getComments()
					}
				})
			},
			onReachBottom(e) {
				console.log('触底加载更多', this.page, this.before_id)
				uni.removeStorage({
					key: 'comments'
				})
				this.getComments()
			},
		}
	}
</script>

<style>
	.uni-page-wrapper {
		height: auto!important;
	}
	.text-content-box {
		padding: 0 15px 0;
		font-size: 16px;
		line-height: 1.35;
		margin-bottom: 10px;
	}
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
