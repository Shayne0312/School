class BoggleGame {
  constructor(boardId, secs = 60) {
    // Game length
    this.secs = secs;
    this.showTimer();

    this.score = 0;
    this.words = new Set();
    this.board = $("#" + boardId);

    // Every 1000 msec, "tick"
    this.timer = setInterval(this.tick.bind(this), 1000);

    $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
  }

  showWord(word) {
    // Show word in the list of words
    $(".words", this.board).append($("<li>", { text: word }));
  }

  showScore() {
    // Show score in HTML
    $(".score", this.board).text(this.score);
  }

  showMessage(msg, cls) {
    // Show a status message
    $(".msg", this.board)
      .text(msg)
      .removeClass()
      .addClass(`msg ${cls}`);
  }

  async handleSubmit(evt) {
    evt.preventDefault();
    const $word = $(".word", this.board);
    let word = $word.val();
    if (!word) return;
    if (this.words.has(word)) {
      this.showMessage(`Already found ${word}`, "err");
      return;
    }

    // Check server for validity
    const resp = await axios.get("/check-word", { params: { word: word } });
    if (resp.data.result === "not-word") {
      this.showMessage(`${word} is not a valid English word`, "err");
    } else if (resp.data.result === "not-on-board") {
      this.showMessage(`${word} is not a valid word on this board`, "err");
    } else {
      this.showWord(word);
      this.score += word.length;
      this.showScore();
      this.words.add(word);
      this.showMessage(`Added: ${word}`, "ok");
    }

    $word.val("").focus();
  }

  showTimer() {
    // Update timer in DOM
    $(".timer", this.board).text(this.secs);
  }

  async tick() {
    this.secs -= 1;
    this.showTimer();
    if (this.secs === 0) {
      clearInterval(this.timer);
      await this.scoreGame();
    }
  }

  async scoreGame() {
    $(".add-word", this.board).hide();
    const resp = await axios.post("/post-score", { score: this.score });
    if (resp.data.brokeRecord) {
      this.showMessage(`New record: ${this.score}`, "ok");
    } else {
      this.showMessage(`Final score: ${this.score}`, "ok");
    }
  }
}