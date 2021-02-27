"use strict";

const accountLink = $("#account")
const registerLink = $("#register")
const loginLink = $("#login")
const logoutLink = $("#logout")
const logBookLink = $("#log_book")


$(document).ready(function() {
    console.log( "ready!" );
    $.get("/user/loggedin", (res) => {
        console.log(res)
        if (res === "true") {
            accountLink.show();
            registerLink.hide();
            loginLink.hide();
            logoutLink.show();
            logBookLink.show();
        }
        else {
            accountLink.hide();
            registerLink.show();
            loginLink.show();
            logoutLink.hide();
            logBookLink.hide();
        }
    })
});
  

