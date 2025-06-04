// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getDatabase } from 'firebase/database';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "",
  authDomain: "snoring-detectionv1.firebaseapp.com",
  databaseURL: "https://snoring-detectionv1-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "snoring-detectionv1",
  storageBucket: "snoring-detectionv1.firebasestorage.app",
  messagingSenderId: "305392375437",
  appId: "1:305392375437:web:cfcdc4478cc7570a7af4c4",
  measurementId: "G-R4SDBYB9QN"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

export { database };