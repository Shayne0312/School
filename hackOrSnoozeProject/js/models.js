"use strict";
const BASE_URL = "https://hack-or-snooze-v3.herokuapp.com";

//******************************************************************************
// Story class represents a single story
class Story {
  constructor({ storyId, title, author, url, username, createdAt }) {
    this.storyId = storyId;
    this.title = title;
    this.author = author;
    this.url = url;
    this.username = username;
    this.createdAt = createdAt;
  }

  // Edit story makes API call to update story on server
  async editStory(user, newData) {
    try {
      const token = user.loginToken;
      const response = await axios({
        method: "PATCH",
        url:  `${BASE_URL}/stories/${this.storyId}` ,
        data: { token, story: newData },
      });
      this.title = response.data.story.title;
      this.author = response.data.story.author;
      this.url = response.data.story.url;
      return this;
    } catch (error) {
      console.error("Error editing story:", error);
    }
  }

  // Get hostname from story URL
  getHostName() {
    return new URL(this.url).host;
  }
}

//******************************************************************************
//List of Story instances: used by UI to show story lists in DOM.
class StoryList {
  constructor(stories) {
    this.stories = stories;
  }

  // Fetches list of stories from API
  static async getStories() {
    try {
      const response = await axios.get( `${BASE_URL}/stories` );
      const stories = response.data.stories.map(story => new Story(story));
      return new StoryList(stories);
    } catch (error) {
      console.error("Error getting stories:", error);
    }
  }

  // Adds new story to list and user's stories
  async addStory(user, { title, author, url }) {
    try {
      const token = user.loginToken;
      const response = await axios({
        method: "POST",
        url:  `${BASE_URL}/stories` ,
        data: { token, story: { title, author, url } },
      });
      const story = new Story(response.data.story);
      this.stories.unshift(story);
      user.ownStories.unshift(story);
      return story;
    } catch (error) {
      console.error("Error adding story:", error);
    }
  }

  // Removes story from list and user favorites/stories
  async removeStory(user, storyId) {
    try {
      const token = user.loginToken;
      await axios({
        url:  `${BASE_URL}/stories/${storyId}` ,
        method: "DELETE",
        data: { token: user.loginToken }
      });

      this.stories = this.stories.filter(story => story.storyId !== storyId);
      user.ownStories = user.ownStories.filter(s => s.storyId !== storyId);
      user.favorites = user.favorites.filter(s => s.storyId !== storyId);
    } catch (error) {
      console.error("Error removing story:", error);
    }
  }
}

//******************************************************************************
// User: a user in the system (only used to represent the current user)
class User {
  constructor({
    username,
    name,
    createdAt,
    favorites = [],
    ownStories = []
  }, token) {
    this.username = username;
    this.name = name;
    this.createdAt = createdAt;
    this.favorites = favorites.map(s => new Story(s));
    this.ownStories = ownStories.map(s => new Story(s));
    this.loginToken = token;
  }

  // Signup makes API call for new user account
  static async signup(username, password, name) {
    try {
      const response = await axios({
        url:  `${BASE_URL}/signup` ,
        method: "POST",
        data: { user: { username, password, name } },
      });
      const { user } = response.data;
      return new User(
        {
          username: user.username,
          name: user.name,
          createdAt: user.createdAt,
          favorites: user.favorites,
          ownStories: user.stories
        },
        response.data.token
      );
    } catch (error) {
      if (error.response.status === 409) {
        throw new Error("Username already taken. Please choose a different username.");
      } else {
        throw new Error("An error occurred during signup. Please try again.");
      }
    }
  }

  // Login makes API call to authenticate user
  static async login(username, password) {
    try {
      const response = await axios({
        url:  `${BASE_URL}/login` ,
        method: "POST",
        data: { user: { username, password } },
      });
      const { user } = response.data;
      return new User(
        {
          username: user.username,
          name: user.name,
          createdAt: user.createdAt,
          favorites: user.favorites,
          ownStories: user.stories
        },
        response.data.token
      );
    } catch (error) {
      if (error.response.status === 401) {
        throw new Error("Incorrect username or password. Please try again.");
      } else {
        throw new Error("An error occurred during login. Please try again.");
      }
    }
  }

  // Update user profile via API call
  async updateUser(username, password) {
    try {
      const token = this.loginToken;
      const newUsername = $("#profile-edit-name").val();
      const response = await axios({
        method: "PATCH",
        url:  `${BASE_URL}/users/${this.username}` ,
        data: { token, user: { username: newUsername, password } },
      });
      this.username = response.data.user.username;
      return this;
    } catch (error) {
      console.error("Error updating user:", error);
    }
  }

  // Get user favorites via API call
  static async loginViaStoredCredentials(token, username) {
    try {
      const response = await axios({
        url:  `${BASE_URL}/users/${username}` ,
        method: "GET",
        params: { token },
      });
      const { user } = response.data;
      return new User(
        {
          username: user.username,
          name: user.name,
          createdAt: user.createdAt,
          favorites: user.favorites,
          ownStories: user.stories
        },
        token
      );
    } catch (error) {
      console.error("loginViaStoredCredentials failed", error);
      return null;
    }
  }

  // Add story from user favorites
  async addFavorite(story) {
    try {
      this.favorites.push(story);
      await this._addOrRemoveFavorite("add", story);
    } catch (error) {
      console.error("Error adding favorite:", error);
    }
  }

  // Remove story from user favorites
  async removeFavorite(story) {
    try {
      this.favorites = this.favorites.filter(s => s.storyId !== story.storyId);
      await this._addOrRemoveFavorite("remove", story);
    } catch (error) {
      console.error("Error removing favorite:", error);
    }
  }

  // Add or remove story from user favorites via API call
  async _addOrRemoveFavorite(newState, story) {
    try {
      const method = newState === "add" ? "POST" : "DELETE";
      const token = this.loginToken;
      await axios({
        url:  `${BASE_URL}/users/${this.username}/favorites/${story.storyId}` ,
        method: method,
        data: { token },
      });
    } catch (error) {
      console.error("Error updating favorite:", error);
    }
  }

  // Check if story is in user favorites
  isFavorite(story) {
    return this.favorites.some(s => s.storyId === story.storyId);
  }
}