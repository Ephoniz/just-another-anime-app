<!-- YourVueComponent.vue -->
<template>
  <div>
    <div v-if="gameStarted">
      <img :src="imageUrl" alt="Anime Character" />
      <div v-if="!gameOver">
        <p>Guess the anime character:</p>
        <input v-model="userGuess" @keyup.enter="submitGuess" />
        <button @click="submitGuess">Submit</button>
        <p v-if="guessResult">{{ guessResult }}</p>
      </div>
      <div v-else>
        <p v-if="hasWon">Congratulations! You guessed right!</p>
        <p v-else>
          Sorry, you lost. The correct answer was: {{ correctAnswer }}
        </p>
        <button @click="startNewGame">Play Again</button>
      </div>
    </div>
    <div v-else>
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
      guessResult: '',
      remainingGuesses: 3
    };
  },
  methods: {
    startGame() {
      this.gameStarted = true;
      this.startNewGame();
    },
    startNewGame() {
      this.gameOver = false;
      this.userGuess = '';
      this.guessResult = '';
      this.remainingGuesses = 3;
      this.fetchRandomAnimeCharacter();
    },
    fetchRandomAnimeCharacter() {
      const path = 'http://127.0.0.1:5000/get_random_anime_character';
      axios
        .get(path) // Assuming your Flask API endpoint is '/get_random_anime_character'
        .then((response) => {
          this.imageUrl = response.data.image_url;
          this.correctAnswer = response.data.correct_answer;
        })
        .catch((error) => {
          console.error('Error fetching random anime character:', error);
        });
    },
    submitGuess() {
      if (this.userGuess.toLowerCase() === this.correctAnswer.toLowerCase()) {
        this.guessResult = 'Congratulations! You guessed right!';
        this.gameOver = true;
      } else {
        this.remainingGuesses--;
        if (this.remainingGuesses === 0) {
          this.guessResult =
            'Sorry, you lost. The correct answer was: ' + this.correctAnswer;
          this.gameOver = true;
        } else {
          this.guessResult =
            'Incorrect guess. You have ' +
            this.remainingGuesses +
            ' guesses remaining.';
        }
      }
    }
  },
  created() {
    this.startGame();
  }
};
</script>

<style>
/* Add your component's styles here if needed */
</style>
