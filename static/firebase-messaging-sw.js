// Import Firebase scripts
importScripts('https://www.gstatic.com/firebasejs/12.18.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/12.18.0/firebase-messaging-compat.js');

//Initialize
firebase.initializeApp({
    apiKey: "AIzaSyC7f-ZoEsun8PH2V0oqnJNnM6HvsZWXvBY",
    authDomain: "nphs-tsa-notifications.firebaseapp.com",
    projectId: "nphs-tsa-notifications",
    storageBucket: "nphs-tsa-notifications.firebasestorage.app",
    messagingSenderId: "552786080626",
    appId: "1:552786080626:web:d76402d87805c3cd5a23eb",
    measurementId: "G-9TBS5HQM01"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    const notificationTitle = payload.data.title;
    const { body, icon, image } = payload.data;

    const notificationOptions = {
        body: body,
        icon:icon,
        image: image
    }
    self.registration.showNotification(notificationTitle, notificationOptions);
});