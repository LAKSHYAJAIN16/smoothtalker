document.addEventListener("DOMContentLoaded", async () => {
  // Initialize States
  const STATES = ["main", "decode", "pickup-lines"];

  // Get the JSON
  fetch("/lines.json").then((response) => console.log(response.body));

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

  function generateRandomPickupLine(){
    return 
  }

  document.getElementById("to-decode-btn").addEventListener("click", () => {
    switchUI("decode");
  });

  document.getElementById("to-pickup-btn").addEventListener("click", () => {
    switchUI("pickup-lines");
  });

  document.getElementById("decode-fn").addEventListener("click", () => {
    decode();
  });
});
