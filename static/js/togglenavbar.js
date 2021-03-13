"use strict";

const logLink = $("#log")
const accountLink = $("#account")
const registerLink = $("#register")
const loginLink = $("#login")
const logoutLink = $("#logout")
const logBookLink = $("#log_book")
const menuLink = $("#menu")


$(document).ready(function() {
    // console.log( "ready!" );
    $.get("/user/loggedin", (res) => {
        console.log("user logged in:", res)
        if (res === "true") {
            logLink.show();
            accountLink.show();
            registerLink.hide();
            loginLink.hide();
            logoutLink.show();
            logBookLink.show();
            menuLink.show()
        }
        else {
            logLink.hide();
            accountLink.hide();
            registerLink.show();
            loginLink.show();
            logoutLink.hide();
            logBookLink.hide();
            menuLink.show()
        }
    })
});
