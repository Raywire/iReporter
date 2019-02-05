module.exports = {
    "parserOptions": {
        "ecmaVersion": 2018
    },
    "extends": "eslint-config-airbnb-base",
    "env": {
        "browser": true,
        "jasmine": true,
        "jest": true,
    },
    "globals": {
        "config": "writeable",
        "user": "writeable",
        "getCookie": "writeable",
        "setCookie": "writeable",
        "logout": "writeable",
        "google": "writeable",
        "showLoader": "writeable",
        "hideLoader": "writeable",
        "moment": "writeable",
        "warningNotification": "writeable",
        "successNotification": "writeable",
        "infoNotification": "writeable",
        "convertToLocalTime": "writeable",
    },
    "rules": {
        "no-unused-vars": [2, { "vars": "local"}],
    }
};