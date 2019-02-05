[![Build Status](https://travis-ci.org/Raywire/iReporter.svg?branch=gh-pages)](https://travis-ci.org/Raywire/iReporter)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f1ca45c570514e38a0f3a16d32a040bc)](https://www.codacy.com/app/Raywire/iReporter?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Raywire/iReporter&amp;utm_campaign=Badge_Grade)

Project: iReporter
Description:iReporter enables any citizen to bring any form of corruption to the notice of appropriate authorities and the
general public. Users can also report on things that needs government intervention.

[GitHub Hosting Link](https://raywire.github.io/iReporter/UI)

## Getting Started

Git clone the repo and cd into the root folder.

### Prerequisites

Node to run the tests
A simple HTTP Server to load the static pages

## Running the app
Cd into the iReporter folder

Run a simple http server using python or node
With Python:

```python
python -m SimpleHTTPServer
```
With Node:

```node
npm install http-server -g
http-server
```
Run the command to install all packages from packages.json

```node
npm install
```

## Running the tests

Tests with coverage are run with jest, puppeteer and coveralls
```node
npm test
```
### Break down into end to end tests

End to end tests check how the front-end integrates with the back-end

## Built With

*   [Vanilla Javascript](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/JavaScript_basics)
*   [Moment.js](https://momentjs.com/)
*   [HTML 5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)

## Author

***Ryan Simiyu***

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
