// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCUunlVa9qWt5OyjyW0TPLLB8_hfM2RjwQ",
  authDomain: "projectskallesh.firebaseapp.com",
  projectId: "projectskallesh",
  storageBucket: "projectskallesh.firebasestorage.app",
  messagingSenderId: "636235805701",
  appId: "1:636235805701:web:0aa4e517ee395c2b91586c",
  measurementId: "G-VN4EM4YXL5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);

// Initialize Google Auth Provider
export const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({
  prompt: 'select_account'
});

// Initialize Cloud Firestore and get a reference to the service
export const db = getFirestore(app);

// Initialize Cloud Storage and get a reference to the service
export const storage = getStorage(app);

export default app;