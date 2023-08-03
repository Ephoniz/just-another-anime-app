<template>
  <div class="main_body">
    <div v-if="gameStarted">
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
        <button ref="playAgainButton" @click="startNewGame">Play Again</button>
      </div>
    </div>
    <div v-else>
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
      <button @click="startGameWithSettings">Start Game</button>
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
      currentRoundGuesses: 0
    };
  },
  methods: {
    startGame() {
      this.gameStarted = true;
      this.startNewGame();
    },
    startGameWithSettings() {
      this.gameStarted = true;
      this.startNewGame();
    },
    startNewGame() {
      this.gameOver = false;
      this.userGuess = '';
      this.message = '';
      this.fetchRandomAnimeCharacter();
      this.countdown = this.guessTime; // Initialize countdown with user's chosen guess time

      clearInterval(this.countdownInterval);

      // Start a new countdown interval
      this.countdownInterval = setInterval(() => {
        this.countdown--;
        if (this.countdown === 0) {
          clearInterval(this.countdownInterval);
          this.submitGuess();
          this.currentRoundGuesses++; // Increment the current round's guess counter

          // Check if the user has reached the maximum number of guesses in the current round
          if (this.currentRoundGuesses >= this.roundLengthAsInt) {
            // Reset the game state to allow the user to choose a new round length
            this.gameStarted = false;
            this.imageUrl = '';
            this.correctAnswer = '';
            this.message = '';
            this.currentRoundGuesses = 0; // Reset the current round's guess counter
          } else {
            // Start a new round if the maximum number of guesses is not reached
            this.startNewGame();
          }
        }
      }, 1000);
    },
    fetchRandomAnimeCharacter() {
      axios
        .get('http://127.0.0.1:5000/get_random_anime_character') // Assuming your Flask API endpoint is '/get_random_anime_character'
        .then((response) => {
          this.imageUrl = response.data.image_url;
          this.correctAnswer = response.data.correct_answer;
        })
        .catch((error) => {
          console.error('Error fetching random anime character:', error);
        });
    },
    submitGuess() {
      const similarityThreshold = 0.4; // Adjust the threshold as needed (0.0 to 1.0)

      const similarity = this.calculateSimilarity(
        this.userGuess,
        this.correctAnswer
      );
      if (similarity >= similarityThreshold) {
        this.message = 'Congratulations! You guessed right!';
        this.gameOver = true;
        this.currentRoundGuesses++; // Increment the current round's guess counter

        // Check if the user has guessed the word correctly in the current round
        if (this.currentRoundGuesses >= this.roundLengthAsInt) {
          // Reset the game state to allow the user to choose a new round length
          this.gameStarted = false;
          this.imageUrl = '';
          this.correctAnswer = '';
          this.message = '';
          this.currentRoundGuesses = 0;
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
      // If the game is already over, start the next round
      if (this.gameOver) {
        this.startNewGame();
        return;
      }

      // Clear the previous message
      this.message = '';

      // If the user input is empty, do nothing
      if (this.userGuess.trim() === '') {
        return;
      }

      // Submit the user's guess
      this.submitGuess();

      // If the game is not over, start the countdown for the next round
      if (!this.gameOver) {
        this.startCountdown();
      }
    },
    toggleModalWithSpace() {
      // Check if the game is not started and the "Play Again" button is visible
      if (this.gameOver) {
        this.startGame();
      }
    },
    stopGame() {
      // Reset the game state to allow the user to choose a new round length
      this.gameStarted = false;
      this.gameOver = false;
      this.imageUrl = '';
      this.correctAnswer = '';
      this.userGuess = '';
      this.message = '';
      this.currentRoundGuesses = 0; // Reset the current round's guess counter
    }
  },
  mounted() {
    let self = this;
    window.addEventListener('keyup', function (e) {
      if (e.key === ' ') {
        self.toggleModalWithSpace(); // declared in your component methods
      }
    });
  },
  updated() {
    let input = document.getElementById('userGuess');
    if (input && !this.gameOver) {
      input.focus();
    }
  },
  computed: {
    // Convert the roundLength to an integer using a computed property
    roundLengthAsInt() {
      return parseInt(this.roundLength);
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
