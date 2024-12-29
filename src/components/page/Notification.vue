<script>
import Vue from "vue";
import LoadScript from "vue-plugin-load-script";

Vue.use(LoadScript);

var firebaseConfig = {
  apiKey: "...",
  authDomain: "...",
  databaseURL: "...",
  projectId: "...",
  storageBucket: "...",
  messagingSenderId: "...",
  appId: "...",
  measurementId: "..."
};

Promise.resolve()
  .then(() =>
    Vue.loadScript(
      "https://www.gstatic.com/firebasejs/7.14.0/firebase-app.js"
    )
  )
  .then(() =>
    Vue.loadScript(
      "https://www.gstatic.com/firebasejs/7.14.0/firebase-messaging.js"
    )
  )
  .then(() =>
    Vue.loadScript(
      "https://www.gstatic.com/firebasejs/7.14.0/firebase-analytics.js"
    )
  )
  .then(() => {
    window.firebase.initializeApp(firebaseConfig);
    const messaging = window.firebase.messaging();
   
  });
</script>