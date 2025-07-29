import { defineStore } from 'pinia'
import { authAxios } from '@/utils/axios'

export const usePostStore = defineStore('posts', {
  state: () => ({
    posts: [],
    userPosts: [],
    loading: false,
    userPostsCache: {}, // { username: { posts: [], lastFetched: timestamp } }
    postsFetched: false,
  }),

  actions: {
    async fetchPosts(force = false) {
      if (this.postsFetched && !force) return
      this.loading = true
      try {
        const response = await authAxios.get('/posts/')
        this.posts = response.data
        this.postsFetched = true
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
          this.userPosts = cache.posts
          return
        }

        const response = await authAxios.get(`/posts/user/${encodeURIComponent(username)}/`)
        this.userPostsCache[username] = {
          posts: response.data,
          lastFetched: now,
        }
        this.userPosts = response.data
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

        const newPost = response.data
        this.posts.unshift(newPost)

        const username = newPost.username || newPost.user?.username
        if (username) {
          // Update live userPosts list
          this.userPosts.unshift(newPost)

          // Update cached userPosts
          if (!this.userPostsCache[username]) {
            this.userPostsCache[username] = {
              posts: [newPost],
              lastFetched: Date.now(),
            }
          } else {
            this.userPostsCache[username].posts.unshift(newPost)
            this.userPostsCache[username].lastFetched = Date.now()
          }
        }

        return newPost
      } catch (error) {
        console.error('Failed to create post:', error)
        throw error
      }
    },

    async deletePost(postId) {
      try {
        await authAxios.delete(`/posts/${postId}/delete/`)
        this.posts = this.posts.filter(post => post.id !== postId)
        this.userPosts = this.userPosts.filter(post => post.id !== postId)
      } catch (error) {
        console.error('Failed to delete post:', error)
      }
    },

    async likePost(postId) {
      try {
        await authAxios.post(`/posts/${postId}/like/`)
        const updatePostArray = (arr) => {
          const index = arr.findIndex(p => p.id === postId)
          if (index !== -1) {
            const post = arr[index]
            post.hasLiked = true
            post.likeCount = (post.likeCount || 0) + 1
            arr.splice(index, 1, { ...post })
          }
        }
        updatePostArray(this.posts)
        updatePostArray(this.userPosts)
      } catch (error) {
        console.error('Failed to like post:', error)
      }
    },

    async unlikePost(postId) {
      try {
        await authAxios.post(`/posts/${postId}/unlike/`)
        const updatePostArray = (arr) => {
          const index = arr.findIndex(p => p.id === postId)
          if (index !== -1) {
            const post = arr[index]
            post.hasLiked = false
            post.likeCount = Math.max((post.likeCount || 1) - 1, 0)
            arr.splice(index, 1, { ...post })
          }
        }
        updatePostArray(this.posts)
        updatePostArray(this.userPosts)
      } catch (error) {
        console.error('Failed to unlike post:', error)
      }
    },

    async repostPost(postId) {
      try {
        await authAxios.post(`/posts/${postId}/repost/`)
        const updatePostArray = (arr) => {
          const index = arr.findIndex(p => p.id === postId)
          if (index !== -1) {
            const post = arr[index]
            post.hasReposted = true
            post.repostCount = (post.repostCount || 0) + 1
            arr.splice(index, 1, { ...post })
          }
        }
        updatePostArray(this.posts)
        updatePostArray(this.userPosts)
      } catch (error) {
        console.error('Failed to repost:', error)
      }
    },

    async undoRepostPost(postId) {
      try {
        await authAxios.delete(`/posts/${postId}/undo_repost/`)
        const updatePostArray = (arr) => {
          const index = arr.findIndex(p => p.id === postId)
          if (index !== -1) {
            const post = arr[index]
            post.hasReposted = false
            post.repostCount = Math.max((post.repostCount || 1) - 1, 0)
            arr.splice(index, 1, { ...post })
          }
        }
        updatePostArray(this.posts)
        updatePostArray(this.userPosts)
      } catch (error) {
        console.error('Failed to undo repost:', error)
      }
    },
  }
})
