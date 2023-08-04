<template>
  <div class="main_body">
    <!-- Show the game only if it has started and the next round countdown is not active -->
    <div v-if="gameStarted && !showNextRoundCountdown">
      <img :src="imageUrl" alt="Anime Character" />
      <div v-if="!gameOver">
        <p>Guess the anime character:</p>
        <input
          id="userGuess"
          v-model="userGuess"
          @keyup.enter="handleUserInput"
        />
        <p v-if="message">{{ message }}</p>
        <p v-if="countdown > 0">Time remaining: {{ countdown }} seconds.</p>
      </div>
      <div v-else>
        <p>{{ message }}</p>
      </div>
    </div>
    <!-- Show the next round countdown only if it's active -->
    <div v-if="showNextRoundCountdown">
      <p>Next round starts in: {{ nextRoundCountdown }} seconds.</p>
    </div>
    <!-- Show the game setup only if the game hasn't started and the next round countdown is not active -->
    <div v-if="!gameStarted && !showNextRoundCountdown">
      <div>
        <label for="guessTimeInput">Enter guess time (in seconds):</label>
        <input type="number" id="guessTimeInput" v-model="guessTime" min="1" />
      </div>
      <div>
        <label for="roundLengthInput"
          >Enter round length (number of guesses):</label
        >
        <input
          type="number"
          id="roundLengthInput"
          v-model="roundLength"
          min="1"
        />
      </div>
      <button @click="startGame">Start Game</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AnimeCharacter',
  data() {
    return {
      gameStarted: false,
      gameOver: false,
      imageUrl: '',
      correctAnswer: '',
      userGuess: '',
      guessTime: 10, // Default guess time in seconds
      roundLength: 10,
      countdown: 0,
      message: '',
      currentRoundGuesses: 0,
      nextRoundCountdown: 0,
      showNextRoundCountdown: false
    };
  },
  methods: {
    startGame() {
      this.gameStarted = true;
      this.showNextRoundCountdown = true; // Show the countdown
      this.nextRoundCountdown = 3; // Initialize the countdown

      const nextRoundInterval = setInterval(() => {
        this.nextRoundCountdown--;
        if (this.nextRoundCountdown === 0) {
          clearInterval(nextRoundInterval);
          this.showNextRoundCountdown = false; // Hide the countdown
          this.startGameRound();
        }
      }, 1000);
    },
    async startNewGame() {
      this.showNextRoundCountdown = true; // Show the countdown
      this.nextRoundCountdown = 3; // Initialize the countdown

      // Fetch the character during the countdown
      const characterData = await this.fetchRandomAnimeCharacter();

      const nextRoundInterval = setInterval(() => {
        this.nextRoundCountdown--;
        if (this.nextRoundCountdown === 0) {
          clearInterval(nextRoundInterval);
          this.showNextRoundCountdown = false; // Hide the countdown

          // Apply the fetched character data
          this.applyCharacterData(characterData);

          this.startGameRound();
        }
      }, 1000);
    },
    applyCharacterData(characterData) {
      this.imageUrl = characterData.imageUrl;
      this.correctAnswer = characterData.correctAnswer;
    },
    startGameRound() {
      this.$nextTick(async () => {
        this.gameOver = false;
        this.userGuess = '';
        this.message = '';

        this.countdown = this.guessTime; // Start the countdown after the image is loaded

        clearInterval(this.countdownInterval);

        const end = Date.now() + this.guessTime * 1000;

        if (this.currentRoundGuesses === 0) {
          const characterData = await this.fetchRandomAnimeCharacter();
          this.applyCharacterData(characterData);
        }

        this.countdownInterval = setInterval(() => {
          const now = Date.now();
          if (now >= end) {
            clearInterval(this.countdownInterval);
            this.submitGuess();
            this.currentRoundGuesses++;
            if (this.currentRoundGuesses >= this.roundLength) {
              this.resetGame();
            } else if (!this.gameOver) {
              this.startNewGame();
            }
          } else {
            this.countdown = Math.ceil((end - now) / 1000);
          }
        }, 100);
      });
    },
    async fetchRandomAnimeCharacter() {
      try {
        const response = await axios.get(
          'http://127.0.0.1:5000/get_random_anime_character'
        );
        return {
          imageUrl: response.data.image_url,
          correctAnswer: response.data.correct_answer
        };
      } catch (error) {
        console.error('Error fetching random anime character:', error);
      }
    },
    submitGuess() {
      const similarityThreshold = 0.4;
      const similarity = this.calculateSimilarity(
        this.userGuess,
        this.correctAnswer
      );
      if (similarity >= similarityThreshold) {
        this.message = 'Congratulations! You guessed right!';
        this.gameOver = true;
        clearInterval(this.countdownInterval); // Stop the timer
        this.currentRoundGuesses++;
        if (this.currentRoundGuesses >= this.roundLength) {
          this.resetGame();
        } else {
          this.startNewGame(); // Start a new game immediately
        }
      } else {
        this.message = 'Incorrect guess. Try again or enter a new guess.';
      }
    },
    calculateSimilarity(str1, str2) {
      // Function to calculate the Levenshtein distance between two strings
      function levenshteinDistance(a, b) {
        const m = a.length;
        const n = b.length;
        const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));

        for (let i = 1; i <= m; i++) dp[i][0] = i;
        for (let j = 1; j <= n; j++) dp[0][j] = j;

        for (let i = 1; i <= m; i++) {
          for (let j = 1; j <= n; j++) {
            if (a[i - 1] === b[j - 1]) dp[i][j] = dp[i - 1][j - 1];
            else
              dp[i][j] =
                Math.min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]) + 1;
          }
        }

        return dp[m][n];
      }

      // Calculate the Levenshtein distance and convert it to a similarity score
      const distance = levenshteinDistance(
        str1.toLowerCase(),
        str2.toLowerCase()
      );
      const maxLength = Math.max(str1.length, str2.length);
      const similarity = 1 - distance / maxLength;

      return similarity;
    },
    handleUserInput() {
      if (this.gameOver) {
        this.startNewGame();
        return;
      }
      this.message = '';
      if (this.userGuess.trim() === '') {
        return;
      }
      this.submitGuess();
    },
    toggleModalWithSpace() {
      if (this.gameOver) {
        this.startGame();
      }
    },
    resetGame() {
      this.gameStarted = false;
      this.imageUrl = '';
      this.correctAnswer = '';
      this.message = '';
      this.currentRoundGuesses = 0;
    }
  },
  mounted() {
    let self = this;
    window.addEventListener('keyup', function (e) {
      if (e.key === ' ') {
        self.toggleModalWithSpace();
      }
    });
  },
  updated() {
    let input = document.getElementById('userGuess');
    if (input && !this.gameOver) {
      input.focus();
    }
  }
};
</script>

<style>
.main_body {
  width: 100%;
  height: 100%;
}
</style>
