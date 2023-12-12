document.addEventListener("DOMContentLoaded", async () => {
  // Initialize States
  const STATES = ["main", "decode", "pickup-lines", "mws", "minsta"];

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

  document.getElementById("my-select").addEventListener("change", function () {
    console.log("You selected: ", this.value);
    localStorage.setItem("f", this.value);
  });

  // Set the default value for the select
  const f = localStorage.getItem("f") || "Teenage (mixed)";
  const children = document.getElementById("my-select").children;
  for (let id = 0; id < children.length; id++) {
    const child = children[id];
    if (child.innerText === f) {
      child.selected = true;
      break;
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
        //We're on whatsapp boiz!
      }

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
        console.log("ran");
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
                  // console.log("Standard Whatsapp Detected");
                  continue;
                } else {
                  //Sometimes the label might contain the convo name, for direct messages
                  if (label.includes(convoTitle)) {
                    isYou = false;
                    continue;
                  } else {
                    // ABORT ABORT
                    // console.log("MSG by User DETECTED");
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
            // console.log(err);
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

      function new_injection() {
        // Actual ChatGPT
        function a_click(e) {
          console.log("clicked!");

          // Get text
          const text = e.target.parentElement.firstChild.innerHTML;
          console.log(text);
          // e.target.parentElement.parentElement.parentElement.innerHTML = "<span id='pasta'>Loading....</span>";

          const body = `
            Write the most attractive, funny reply you can think of. The text message is : ${text}
          `;
          console.log(body);

          fetch(`https://free-gpt-4-api.meet508.tech/?text=${body}`)
            // Retry
            .catch((g) => {
              fetch(`https://free-gpt-4-api.meet508.tech/?text=${body}`, {
                method: "GET",
                cache: "default",
              })
                .then((e) => {
                  return e.text();
                })
                .then((f) => {
                  console.log(f);
                  const txt = f.choices[0].text;
                  console.log(txt);
                  e.target.parentElement.innerHTML = `<span>${text}</span><span style='color: #bf0407; font-weight : bold;'>${txt}</span><br><br><button style="font-size : 20px; border-radius : 25px; padding-left : 3px; padding-right : 3px;
              padding-top : 3px; padding-bottom : 3px; background-color : lightblue;">😉</button>`;
                });
            })
            // Get Text
            .then((e) => {
              console.log(e);
              return e.text();
            })
            .then((f) => {
              console.log(f);
              const txt = f;
              console.log(txt);
              e.target.parentElement.innerHTML = `<span>${text}</span><span style='color: #bf0407; font-weight : bold;'>${txt}</span><br><br><button style="font-size : 20px; border-radius : 25px; padding-left : 3px; padding-right : 3px;
              padding-top : 3px; padding-bottom : 3px; background-color : lightblue;">😉</button>`;
            });
        }

        // console.log("les go");
        const boiz = document.getElementsByClassName("_21Ahp");
        for (let i = 0; i < boiz.length; i++) {
          const boi = boiz[i];

          // get our span
          const spans = boi.children;
          for (let k = 0; k < spans.length; k++) {
            const element = spans[k];
            if (
              element.innerText !== null &&
              element.innerText !== "" &&
              element.innerText !== undefined
            ) {
              // It's our boi!
              if (element.innerHTML.includes("button")) {
                break;
              } else {
                element.onclick = a_click;
                element.innerHTML = `<span>${element.innerText}</span><br><br><button style="font-size : 20px; border-radius : 25px; padding-left : 3px; padding-right : 3px;
                padding-top : 3px; padding-bottom : 3px; background-color : lightblue;">😉</button>`;
              }
            }
          }
        }

        //Repeat every 3 seconds for new messages
        setTimeout(new_injection, 3000);
      }

      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id, allFrames: true },
          function: injection,
        });
      });
    });
  }

  function monitorInstagram() {
    // x1n2onr6
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      let url = new URL(tabs[0].url);
      if (url.host !== "www.instagram.com") {
        alert("You are not on Insta");
      } else {
        //We're on whatsapp boiz!
      }

      let iters = 0;
      chrome.runtime.onMessage.addListener(function (request, sender) {
        if (request.action == "getSource") {
          // this.pageSource = request.source;
          const html = request.source;
          const xs = html.split("->->->->->:-!");

          //Update Iters
          iters += 1;

          //Write to Output
          document.getElementById(
            "minsta-iters"
          ).innerText = `Iters : ${iters}`;
          document.getElementById("minsta-content").innerHTML = xs[1];

          //Save to localStorage
          // document.getElementById("minsta").innerText = ("Monitoring Chat with " + xs[0] + " .....");
          localStorage.setItem("minsta", html);
        }
      });

      function injection() {
        //Get Title of Conversation
        const convoThings = document.querySelectorAll(
          ".x1lliihq.x193iq5w.x6ikm8r.x10wlt62.xlyipyv.xuxw1ft"
        )
        if(convoThings.length == 0) return;

        const convoTitle = convoThings[convoThings.length - 1].innerText;

        //Get All Messages
        const messages = document.querySelectorAll(
          ".x6prxxf.x1fc57z9.x1yc453h.x126k92a"
        );

        const actMsgs = [];
        let op = false;
        for (let i = 0; i < messages.length; i++) {
          try {
            //Get Text
            const txt = messages[i].innerText;

            //Check if it is our message
            let isYou = false;
            if(messages[i].classList.contains("xzsf02u")){
              isYou = false;
            }
            else{
              isYou = true;
            }

            // If we have something open and we're the user, close
            if(isYou === true && actMsgs.length === 0){
              // sorry
            }
            else{
              if(isYou === true){
                actMsgs[actMsgs.length - 1]["messages_us"].push(txt)
                op = false;
              }
              if(isYou === false && op === true){
                actMsgs[actMsgs.length - 1]["messages_other"].push(txt)
              }
              if(isYou === false && op === false){
                actMsgs.push({messages_other : [txt], messages_us : []});
                op = true;
              }
            }
          } catch (err) {
            // Our Message, so don't do anything
            // console.log(err);
          }
        }

        // Persistance because.... WHY NOT?
        const act = JSON.parse(localStorage.getItem("smoothtalker_buf_insta" || "[]")) || [];
        const new_act = [... new Set(act.concat(actMsgs))];

        //Create LS Output
        localStorage.setItem("smoothtalker_buf_insta", JSON.stringify(new_act));

        chrome.runtime.sendMessage({
          action: "getSource",
          source: convoTitle + "->->->->->:-!" + JSON.stringify({
            new_act
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
    });
  }

  function saveMWSData() {
    //Get JSON data
    const data = localStorage.getItem("mws");
    saveTextAs(data, "all_whatsapp_messages.json");
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

  document.getElementById("to-minsta-btn").addEventListener("click", () => {
    switchUI("minsta");
    monitorInstagram();
  });

  document.getElementById("to-mws-btn").addEventListener("click", () => {
    switchUI("mws");
    monitorWhatsapp();
  });

  document.getElementById("mws-export").addEventListener("click", () => {
    saveMWSData();
  });

  document.getElementById("decode-fn").addEventListener("click", () => {
    decode();
  });
});
