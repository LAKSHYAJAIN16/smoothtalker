document.addEventListener("DOMContentLoaded", async () => {
  // Initialize States
  const STATES = ["main", "decode", "pickup-lines", "mws"];
  let scroll = false;

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
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      let url = new URL(tabs[0].url);

      if (url.host !== "web.whatsapp.com") {
        alert("You are not on WhatsApp");
      } else {
      }
    });

    let iters = 0;
    chrome.runtime.onMessage.addListener(function (request, sender) {
      if (request.action == "getSource") {
        // this.pageSource = request.source;
        const html = request.source;

        //Update Iters
        iters += 1;

        //Write to Output
        document.getElementById("mws-iters").innerText = `Iters : ${iters}`;
        document.getElementById("mws-content").innerText = html;

        //Save to localStorage
        localStorage.setItem("mws", html);
      }
    });

    function injection() {
      //Get Title of Conversation
      const convoTitle = document.querySelector("._21nHd").innerText;

      //Get All Messages
      const msgs = document.getElementsByClassName("_1Gy50");
      const actMsgs = [];
      let lastName = "";
      for (let i = 0; i < msgs.length; i++) {
        //Get Actual Message
        const msg = msgs[i].firstChild.firstChild;

        try {
          //Get Name
          const par = msgs[i].parentNode;
          const supPar = par.parentNode;
          const container = supPar.firstChild;
          const nameElement = container.firstChild;
          let name = nameElement.innerText || msg.innerText;

          //Check if it is our message
          const youContainer = supPar.parentNode;
          const spans = youContainer.childNodes;
          let isYou = false;
          for (let i = 0; i < spans.length; i++) {
            const element = spans[i];
            // Check if it is a span
            if (element.nodeName === "SPAN") {
              const label = element.ariaLabel;
              // console.log(label);
              if (label === null || undefined) {
                //Nothing. Standard Whatsapp
                console.log("Standard Whatsapp Detected");
                continue;
              } else {
                //Sometimes the label might contain the convo name, for direct messages
                if (label.includes(convoTitle)) {
                  isYou = false;
                  continue;
                } else {
                  // ABORT ABORT
                  console.log("MSG by User DETECTED");
                  isYou = true;
                  break;
                }
              }
            }
          }

          if (isYou === true) {
            console.log("Message by User detected");
            // Abort!
          } else if (isYou === false) {
            //If the name and sender are equal, take the last valid name (WhatsApp :L)
            if (name === msg.innerText) {
              name = lastName;
            } else if (name !== msg.innerText) {
              lastName = name;
            }

            //If the name is blank, we're in a direct chat, so the name will be the title
            if (name === "") {
              name = convoTitle;
              lastName = convoTitle;
            }

            //Assign each message a unique id according to the message and name
            actMsgs.push({ sender: name, msg: msg.innerText });
          }
        } catch (err) {
          // Our Message, so don't do anything
          console.log(err);
        }
      }

      //Format
      const output = {
        title: convoTitle,
        msgs: actMsgs,
      };

      //Write to localStorage
      const storage = JSON.parse(
        localStorage.getItem("smoothtalker_buf") || "[]"
      );

      //Create LS Output
      let ls_output = [];
      let found = false;
      for (let i = 0; i < storage.length; i++) {
        let chat = storage[i];
        let nChat = {};
        let c_msgs = chat.msgs;

        nChat.title = chat.title;
        if (chat.title === output.title) {
          console.log(`Updated Smoothtalker Data for ${convoTitle}`);
          //Append
          c_msgs = c_msgs.concat(output.msgs);

          //Remove duplicates
          let unique_msgs = [];
          for (let i = 0; i < c_msgs.length; i++) {
            const msg = c_msgs[i];
            let is_unique = true;
            for (let j = 0; j < unique_msgs.length; j++) {
              const unique_msg = unique_msgs[j];
              if (
                msg.sender === unique_msg.sender &&
                msg.msg === unique_msg.msg
              ) {
                is_unique = false;
              }
            }

            if (is_unique === true) {
              unique_msgs.push(msg);
            }
          }
          c_msgs = unique_msgs;

          //Set found to true
          found = true;
        }
        nChat.msgs = c_msgs;
        ls_output.push(nChat);
      }

      //If our chat isn't a part, add it
      if (found === false) {
        ls_output.push(output);
      }

      localStorage.setItem("smoothtalker_buf", JSON.stringify(ls_output));

      chrome.runtime.sendMessage({
        action: "getSource",
        source: JSON.stringify({
          ls_output,
        }),
      });

      //Repeat every 3 seconds for new messages
      setTimeout(injection, 3000);
    }

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id, allFrames: true },
        function: injection,
      });
    });
  }

  function saveMWSData() {
    //Get JSON data
    const data = localStorage.getItem("mws");
    saveTextAs(data, "all_whatsapp_messages.json");
  }

  function mwsScrollUp(){
    window.scrollBy(0, -100);
    if(scroll === true){
      setTimeout(mwsScrollUp, 1000);
    }
    else if(scroll === false){
      // Stop Timeout loop
    }
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

  document.getElementById("mws-export").addEventListener("click", () => {
    saveMWSData();
  });

  document.getElementById("mws-scrollUp").addEventListener("keydown", (e) => {
    if(e.key === "q"){
      scroll = true;
      mwsScrollUp();
    }
    else if(e.key === "z"){
      scroll = false;
    }
  });

  document.getElementById("decode-fn").addEventListener("click", () => {
    decode();
  });
});
