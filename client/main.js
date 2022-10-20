document.addEventListener("DOMContentLoaded", async () => {
  // Initialize States
  const STATES = ["main", "decode", "pickup-lines", "mws"];

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

  function monitorWhatsapp() {
    console.log(window.location.href);
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      let url = new URL(tabs[0].url);

      if (url.host !== "web.whatsapp.com") {
        alert("You are not on WhatsApp");
      } else {
      }
    });

    chrome.runtime.onMessage.addListener(function (request, sender) {
      if (request.action == "getSource") {
        this.pageSource = request.source;
        const html = request.source;
        alert(html);
      }
    });

    function injection() {
      //Get Title of Conversation
      const convoTitle = document.querySelector("._21nHd").innerText;

      //Get All Names
      const names = document.getElementsByClassName("a71At");
      const actNames = [];
      for (let i = 0; i < names.length; i++) {
        const name = names[i];
        actNames.push(name.innerText);
      }

      //Get All Messages
      const msgs = document.getElementsByClassName("_1Gy50");
      const actMsgs = [];
      for (let i = 0; i < msgs.length; i++) {
        const msg = msgs[i].firstChild.firstChild;
        actMsgs.push(msg.innerText);
      }

      //Format
      const output = {
        title: convoTitle,
        msgs: [],
      };
      for (let k = 0; k < names.length; k++) {
        output.msgs.push({ sender: actNames[k], msg: actMsgs[k] });
      }

      chrome.runtime.sendMessage({
        action: "getSource",
        source: JSON.stringify(output),
      });
    }

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id, allFrames: true },
        function: injection,
      });
    });
  }

  function generateRandomPickupLine() {
    return;
  }

  document.getElementById("to-decode-btn").addEventListener("click", () => {
    switchUI("decode");
  });

  document.getElementById("to-pickup-btn").addEventListener("click", () => {
    switchUI("pickup-lines");
  });

  document.getElementById("to-mws-btn").addEventListener("click", () => {
    switchUI("mws");
    monitorWhatsapp();
  });

  document.getElementById("decode-fn").addEventListener("click", () => {
    decode();
  });
});
