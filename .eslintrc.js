module.exports = {
    "parserOptions": {
        "ecmaVersion": 2018
    },
    "extends": "eslint-config-airbnb-base",
    "globals": {
        "config": true,
        "user":true,
        "window": true,
        "document": true,
        "google": true,
        "getCookie": true,
        "setCookie": true,
        "setTimeout": true,
        "logout": true,
        "showLoader": true,
        "hideLoader": true,
        "moment": true,
        "warningNotification": true,
        "successNotification": true,
        "convertToLocalTime": true,
        "localStorage": true,
        "fetch": true,
        "Request": true,
        "Headers": true,
        "FormData": true,
        "console": true,
    },
    "rules": {
        "no-unused-vars": [1, { "vars": "local"}],
    }
};