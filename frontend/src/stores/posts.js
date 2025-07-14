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
        const index = this.posts.findIndex(p => p.id === postId)
        if (index !== -1) {
          const updated = { ...this.posts[index] }
          updated.likeCount += 1
          updated.hasLiked = true
          this.posts.splice(index, 1, updated)
        }
      } catch (error) {
        console.error('Failed to like post:', error)
      }
    },

    async unlikePost(postId) {
      try {
        await authAxios.post(`/posts/${postId}/unlike/`)
        const index = this.posts.findIndex(p => p.id === postId)
        if (index !== -1) {
          const updated = { ...this.posts[index] }
          updated.likeCount = Math.max(updated.likeCount - 1, 0)
          updated.hasLiked = false
          this.posts.splice(index, 1, updated)
        }
      } catch (error) {
        console.error('Failed to unlike post:', error)
      }
    },

    async repostPost(postId) {
      try {
        await authAxios.post(`/posts/${postId}/repost/`)
        const index = this.posts.findIndex(p => p.id === postId)
        if (index !== -1) {
          const updated = { ...this.posts[index] }
          updated.repostCount += 1
          updated.hasReposted = true
          this.posts.splice(index, 1, updated)
        }
      } catch (error) {
        console.error('Failed to repost:', error)
      }
    },

    async undoRepostPost(postId) {
      try {
        await authAxios.delete(`/posts/${postId}/undo_repost/`)
        const index = this.posts.findIndex(p => p.id === postId)
        if (index !== -1) {
          const updated = { ...this.posts[index] }
          updated.repostCount = Math.max(updated.repostCount - 1, 0)
          updated.hasReposted = false
          this.posts.splice(index, 1, updated)
        }
      } catch (error) {
        console.error('Failed to undo repost:', error)
      }
    }
  }
})