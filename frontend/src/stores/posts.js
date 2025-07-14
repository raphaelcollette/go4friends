import { defineStore } from 'pinia'
import { authAxios } from '@/utils/axios'

export const usePostStore = defineStore('posts', {
  state: () => ({
    posts: [],
    loading: false,
  }),

  actions: {
    async fetchPosts() {
      this.loading = true
      try {
        const response = await authAxios.get('/posts/')
        this.posts = response.data
      } catch (error) {
        console.error('Failed to fetch posts:', error)
      } finally {
        this.loading = false
      }
    },

    async createPost(content, isAnonymous = false, clubId = null) {
      try {
        const response = await authAxios.post('/posts/create/', {
          content,
          is_anonymous: isAnonymous,
          club: clubId,
        })
        this.posts.unshift(response.data)
      } catch (error) {
        console.error('Failed to create post:', error)
        throw error
      }
    },

    async deletePost(postId) {
      try {
        await authAxios.delete(`/posts/${postId}/delete/`)
        this.posts = this.posts.filter(post => post.id !== postId)
      } catch (error) {
        console.error('Failed to delete post:', error)
      }
    },

    async likePost(postId) {
      try {
        await authAxios.post(`/posts/${postId}/like/`)
        await this.fetchPosts()
      } catch (error) {
        console.error('Failed to like post:', error)
      }
    },

    async unlikePost(postId) {
      try {
        await authAxios.post(`/posts/${postId}/unlike/`)
        await this.fetchPosts()
      } catch (error) {
        console.error('Failed to unlike post:', error)
      }
    },

    async repostPost(postId) {
      try {
        await authAxios.post(`/posts/${postId}/repost/`)
        await this.fetchPosts()
      } catch (error) {
        console.error('Failed to repost post:', error)
      }
    },

    async undoRepostPost(postId) {
      try {
        await authAxios.post(`/posts/${postId}/undo_repost/`)
        await this.fetchPosts()
      } catch (error) {
        console.error('Failed to undo repost:', error)
      }
    },
  }
})