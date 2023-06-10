//// Make a fetch request to the Firebase Storage REST API to get the list of images
//fetch('gs://competition-a5c93.appspot.com/')
//    .then(response => response.json())
//    .then(data => {
//        // Extract the image URLs from the response
//        var images = data.items.map(item => item.mediaLink);
//
//        // Loop through the images array and create an img element for each image
//        for (var i = 0; i < images.length; i++) {
//            var img = document.createElement('img');
//            img.src = images[i];
//            img.classList.add("cardimg");
//            document.querySelector(".cards").appendChild(img);
//        }
//    })
//    .catch(error => {
//        console.error('Error:', error);
//    });

//function displayImages(imageUrls) {
//        var gallery = document.querySelector(".cards");
//
//        imageUrls.forEach(function(url) {
//          var img = document.createElement("img");
//          img.src = url;
//          gallery.appendChild(img);
//        });
//      }
//
//      var imageUrls = { image_urls tojson() };
//displayImages(imageUrls);


// For Firebase JS SDK v7.20.0 and later, measurementId is optional
// const firebaseConfig = {
//     apiKey: "AIzaSyAnhloXy_qVpeLDydEkAQ878aYPoSuW1q4",
//     authDomain: "competition-a5c93.firebaseapp.com",
//     databaseURL: "https://competition-a5c93-default-rtdb.firebaseio.com",
//     projectId: "competition-a5c93",
//     storageBucket: "competition-a5c93.appspot.com",
//     messagingSenderId: "72680403206",
//     appId: "1:72680403206:web:1262babdacad10df71ae87",
//     measurementId: "G-CNL7R6TF4L",
//     serviceAccount: "udjatservicekey.json"
// };

// firebase.initializeApp(firebaseConfig);

// // Get a reference to the Firebase Storage bucket
// const storageRef = firebase.storage().ref();

// // Get a reference to the image container
// const imageContainer = document.getElementById("image-container");

// // Loop through all the images in the bucket and display them
// storageRef.listAll().then(function (result) {
//     result.items.forEach(function (imageRef) {
//         // Get the download URL for the image
//         imageRef.getDownloadURL().then(function (url) {
//             // Create an <img> element and set its source to the download URL
//             const img = document.createElement("img");
//             img.src = url;

//             // Append the <img> element to the image container
//             imageContainer.appendChild(img);
//         });
//     });
// });