document.addEventListener("DOMContentLoaded", async () => {
  const STATES = ["main", "decode"];

  function switchUI(uiState) {
    console.log("switching to ", uiState);
    for (let i = 0; i < STATES.length; i++) {
      const element = document.getElementById(STATES[i]);
      if (element.id === uiState) {
        element.style.display = "inherit";
      } else {
        element.style.display = "none";
      }
    }
  }

  function decode() {
    const val = document.getElementById("decodeInput").innerText;

    //Send to Backend??
  }

  document.getElementById("to-decode-btn").addEventListener("click", () => {
    switchUI("decode");
  });

  document.getElementById("decode-fn").addEventListener("click", () => {
    decode();
  });
});
