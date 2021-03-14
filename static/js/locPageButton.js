"use strict";

const newBookButton = $("#new-book")
const newBookForm = $("#new-book-form")


$.get("/user/loggedin", (res) => {
    console.log("user logged in:", res)
    if (res === "false") {
        newLocButton.hide();
        newLocForm.hide();
    }
    else {
        newLocButton.show();
        saveButton.show();
    }
});

// function toggleBookForm() {
// var x = document.getElementById("new-book-form");
// if (x.style.display === "none") {
//     x.style.display = "block";
// } else {
//     x.style.display = "none";
// }
// }

newBookButton.on("click", () => {
    newBookForm.show();
        
});
