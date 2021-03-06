"use strict";

const newLocButton = $("#new-loc")
const newLocForm = $("#new-loc-form")
const saveButton = $("#save-button")
const readButton = $("#read-button")
const unsaveButton = $("#unsave-button")
const unreadButton = $("#unread-button")

// Grab pathname from browser
const path1 = window.location.pathname

// Slice pathname string to just include the book_id
const book_id1 = path1.slice(7)
console.log('book_id:', book_id1)


// function toggleLocForm() {
//     var x = document.getElementById("new-loc-form");
//     if (x.style.display === "none") {
//       x.style.display = "block";
//     } else {
//       x.style.display = "none";
//     }
//   }

$.get("/user/loggedin", (res) => {
    // console.log("user logged in:", res)
    if (res === "false") {
        newLocButton.hide();
        saveButton.hide();
        unsaveButton.hide();
        readButton.hide();
        unreadButton.hide();
    }
    else {
        newLocButton.show();
        saveButton.show();
        unsaveButton.show();
        readButton.show();
        unreadButton.show();
    }
});

$.get(`/user/is-book-saved/${book_id1}`, (res) => {
    if (res.read === true) {
        saveButton.hide();
        unsaveButton.show();
        readButton.hide();
        unreadButton.show();
    } else if (res.saved === true) {
        saveButton.hide();
        unsaveButton.show();
    }
});

newLocButton.on("click", () => {
        newLocForm.show();
        });
});

saveButton.on("click", () => {
    $.post("/user/save-book", {book_id: book_id1}, (res) => {
        saveButton.hide();
        unsaveButton.show()
        });
});

unsaveButton.on("click", () => {
    $.post("/user/unsave-book", {book_id: book_id1}, (res) => {
        unsaveButton.hide();
        saveButton.show()
        readButton.show()
        unreadButton.hide()
        });
});

readButton.on("click", () => {
    $.post("/user/read-book", {book_id: book_id1}, (res) => {
        readButton.hide();
        saveButton.hide();
        unsaveButton.show();
        unreadButton.show()
        });
});

unreadButton.on("click", () => {
    $.post("/user/unread-book", {book_id: book_id1}, (res) => {
        unreadButton.hide();
        readButton.show();
        });
});