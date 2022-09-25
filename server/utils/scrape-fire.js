// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore, getDocs, collection } from "firebase/firestore";

import { writeFileSync, readFileSync} from "fs";

const fn = async () => {
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyDLlpqRWjsd8WkBq9Y-A-tlQfIXwE_Wh60",
    authDomain: "itsalright-e6062.firebaseapp.com",
    projectId: "itsalright-e6062",
    storageBucket: "itsalright-e6062.appspot.com",
    messagingSenderId: "451606941252",
    appId: "1:451606941252:web:fae20fb51769229e683611",
    measurementId: "G-4421CQ6M2N",
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const db = getFirestore(app);

  // Get Docs
  const docs = await getDocs(collection(db, "pickup-lines"));
  const pickuplines = [];
  docs.docs.map((e) => {
    pickuplines.push(e.data());
  });

  console.log(pickuplines);

  // Write to JSON
  writeFileSync("data.json", JSON.stringify(pickuplines));
};

const test = () => {
  const text = readFileSync(
   "server/utils/data copy.json"
  );
  const js = JSON.parse(text);
  console.log(js);
};
test();
// fn();
