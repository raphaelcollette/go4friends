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
        const response = await authAxios.get('/api/posts/')
        this.posts = response.data
      } catch (error) {
        console.error('Failed to fetch posts:', error)
      } finally {
        this.loading = false
      }
    },

    async createPost(content, isAnonymous = false, clubId = null) {
      try {
        const response = await authAxios.post('/api/posts/create/', {
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
        await authAxios.delete(`/api/posts/${postId}/delete/`)
        this.posts = this.posts.filter(post => post.id !== postId)
      } catch (error) {
        console.error('Failed to delete post:', error)
      }
    }
  }
})