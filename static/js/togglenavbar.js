"use strict";

const accountLink = $("#account")
const registerLink = $("#register")
const loginLink = $("#login")
const logoutLink = $("#logout")
const logBookLink = $("#log_book")

$.get("/user/loggedin", (res) => {
    if (res === "true") {
        accountLink.removeClass("hidden");
        registerLink.addClass("hidden");
        loginLink.addClass("hidden");
        logoutLink.removeClass("hidden");
        logBookLink.removeClass("hidden");
    };
});