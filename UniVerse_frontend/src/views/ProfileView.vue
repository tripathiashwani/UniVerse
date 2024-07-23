<template>
    <main class="px-8 py-6 bg-gray-100">
        <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
            <div class="main-left col-span-1 space-y-4">
                <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                    <img :src="avatar_" class="mb-6 rounded-full" />

                    <p><strong>{{ user.name }}</strong></p>
                    <div class="mt-6">
                        <button class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg"
                            @click="sendFriendshipRequest"
                            v-if="userStore.user.id !== user.id && can_send_friendship_request">
                            Send friendship request
                        </button>
                        <button class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg"
                            @click="goToChatRoom" v-if="userStore.user.id !== user.id">
                            Message
                        </button>
                    </div>
                    <div v-if="user.id === userStore.user.id" class="mt-6">
                        <input type="file" @change="handleAvatarChange">
                        <button class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg mt-4"
                            @click="uploadAvatar">
                            Update Avatar
                        </button>
                    </div>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">182 friends</p>
                        <p class="text-xs text-gray-500">120 posts</p>
                    </div>
                </div>
                <div class="main-right col-span-1 space-y-4">
                    <PeopleYouMayKnow />
                    <trends />


                </div>
            </div>

            <div class="main-center col-span-3 space-y-4">
                <div class="bg-white border border-gray-200 rounded-lg" v-if="user.id === userStore.user.id">
                    <form v-on:submit.prevent="submitform" method="post">
                        <div class="p-4">
                            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                                placeholder="What are you thinking about?"></textarea>
                        </div>

                        <div class="p-4 border-t border-gray-100 flex justify-between">
                            <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach
                                image</a>

                            <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                        </div>
                    </form>
                </div>


                <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                    <FeedItem v-bind:post="post" />
                </div>
            </div>


        </div>
    </main>
</template>
<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue';
import Trends from '../components/Trends.vue';
import FeedItem from '../components/FeedItem.vue'
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default {
    name: 'Profileview',
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
    },
    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()
        return {
            userStore,
            toastStore
        }
    },
    data() {
        return {
            posts: [],
            body: '',
            user: {},
            can_send_friendship_request: null,
            selectedFile: null,
            avatar_: ''
        }
    },
    mounted() {
        // this.setavatar()
        this.getFeed()
    },
    watch: {
        '$route.params.id': {
            handler: function () {
                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },
    methods: {
        triggerFileInput() {
            this.$refs.fileInput.click()
        },
        handleFileChange(event) {
            const file = event.target.files[0]
            this.avatar = file
            if (file) {
                // Handle file selection
            }
        },
        triggerAvatarInput() {
            this.$refs.avatarInput.click()
        },
        handleAvatarChange(event) {
            const file = event.target.files[0]
            if (file) {
                this.selectedFile = file
            }
        },
        async uploadAvatar() {
            console.log(this.avatarFile)
            if (this.selectedFile) {
                const formData = new FormData()
                formData.append('avatar', this.selectedFile)

                try {
                    const response = await axios.put('/api/profile_picture/', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                    //   this.userStore.user.avatar = "http://127.0.0.1:8000/api"+response.data.avatar
                    // https://fit-akita-deciding.ngrok-free.app/
                    this.userStore.setUserInfo(response.data)
                    console.log(this.userStore.user.avatar)
                    this.avatar_ = this.userStore.user.avatar

                    this.toastStore.showToast(5000, 'Avatar updated successfully!', 'bg-emerald-300')
                } catch (error) {
                    console.log('error', error)
                    this.toastStore.showToast(5000, 'Failed to update avatar.', 'bg-red-300')
                }
            }
        },
        sendFriendshipRequest() {
            axios
                .post(`/api/friends/${this.$route.params.id}/request/`)
                .then(response => {
                    // console.log('data', response.data)
                    this.can_send_friendship_request = false
                    if (response.data.message == 'request already sent') {
                        this.toastStore.showToast(5000, 'The request has already been sent!', 'bg-red-300')
                    } else {
                        this.toastStore.showToast(5000, 'The request was sent!', 'bg-emerald-300')
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data.posts)
                    this.posts = response.data.posts
                    this.user = response.data.user
                    this.can_send_friendship_request = response.data.can_send_friendship_request
                    this.avatar_ = "https://fit-akita-deciding.ngrok-free.app/api" + response.data.user.avatar
                })
                .catch(error => {
                    console.log('error_hai', error)
                })
        },
        goToChatRoom() {
            const currentUserID = this.userStore.user.id
            const profileUserID = this.$route.params.id
            const roomID = currentUserID < profileUserID ? `${currentUserID}_${profileUserID}` : `${profileUserID}_${currentUserID}`
            this.$router.push({ name: 'ChatRoom', params: { roomID } })
        },
        deletePost(id) {
            this.posts = this.posts.filter(post => post.id !== id)
        },
        submitform() {
            axios
                .post('/api/posts/create/', { 'body': this.body })
                .then(response => {
                    // console.log('data', response.data)
                    this.posts.push(response.data)
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        likePost(id) {
            axios
                .post(`/api/posts/${id}/like/`)
                .then(response => {
                    if (response.data.message == "liked") {
                        this.post.likes_count += 1;
                        // this.color="#FF0000";
                    }
                    else {
                        this.post.likes_count -= 1;
                        // this.color="#ffffff";
                    }
                })
                .catch(error => {
                    console.log("error", error);
                });
        },

    }
}
</script>
