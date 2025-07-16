import { defineStore } from 'pinia'
import { authAxios } from '@/utils/axios'

export const usePostStore = defineStore('posts', {
  state: () => ({
    posts: [],
    loading: false,
    userPostsCache: {}, // { username: { posts: [], lastFetched: timestamp } }
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

    async fetchUserPosts(username, force = false) {
      this.loading = true
      try {
        const now = Date.now()
        const cache = this.userPostsCache[username]
        const fresh = cache && (now - cache.lastFetched) < 60000

        if (!force && fresh) {
          this.posts = cache.posts
          return
        }

        const response = await authAxios.get(`/posts/user/${encodeURIComponent(username)}/`)
        this.userPostsCache[username] = {
          posts: response.data,
          lastFetched: now,
        }
        this.posts = response.data
      } catch (error) {
        console.error('Failed to fetch user posts:', error)
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
          const post = this.posts[index]
          post.hasLiked = true
          post.likeCount = (post.likeCount || 0) + 1
          this.posts.splice(index, 1, { ...post })
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
          const post = this.posts[index]
          post.hasLiked = false
          post.likeCount = Math.max((post.likeCount || 1) - 1, 0)
          this.posts.splice(index, 1, { ...post })
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
          const post = this.posts[index]
          post.hasReposted = true
          post.repostCount = (post.repostCount || 0) + 1
          this.posts.splice(index, 1, { ...post })
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
          const post = this.posts[index]
          post.hasReposted = false
          post.repostCount = Math.max((post.repostCount || 1) - 1, 0)
          this.posts.splice(index, 1, { ...post })
        }
      } catch (error) {
        console.error('Failed to undo repost:', error)
      }
    },
  }
})
