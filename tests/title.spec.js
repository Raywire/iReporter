import puppeteer from 'puppeteer';

const appUrlBase = 'https://raywire.github.io/iReporter/UI';
const INDEX = `${appUrlBase}/index.html`;
const ABOUT = `${appUrlBase}/about.html`;
const SIGNIN = `${appUrlBase}/signin.html`;
const SIGNUP = `${appUrlBase}/signup.html`;
const RESET_REQUEST = `${appUrlBase}/reset_request.html`;
const RESET_PASSWORD = `${appUrlBase}/reset_password.html`;
const CONTACT = `${appUrlBase}/contact.html`;

let page;
let browser;

beforeAll(async () => {
    browser = await puppeteer.launch();
    page = await browser.newPage();
});
afterAll(() => {
    browser.close();
});
describe('Testing the Title in Sign Up Page', () => {
    test('assert that <title> is correct', async () => {
        await page.goto(SIGNUP);
        const title = await page.title();
        expect(title).toBe(
            'iReporter Sign Up'
        );
    });
});

describe('Testing the Title in Sign In Page', () => {
    test('assert that <title> is correct', async () => {
        await page.goto(SIGNIN);
        const title = await page.title();
        expect(title).toBe(
            'iReporter Sign In'
        );
    });
});

describe('Testing the Title in Request Password Reset Page', () => {
    test('assert that <title> is correct', async () => {
        await page.goto(RESET_REQUEST);
        const title = await page.title();
        expect(title).toBe(
            'iReporter Request Password Reset'
        );
    });
});

describe('Testing the Title in Reset Password Page', () => {
    test('assert that <title> is correct', async () => {
        await page.goto(RESET_PASSWORD);
        const title = await page.title();
        expect(title).toBe(
            'iReporter Password Reset'
        );
    });
});

describe('Testing the Title in Contact Page', () => {
    test('assert that <title> is correct', async () => {
        await page.goto(CONTACT);
        const title = await page.title();
        expect(title).toBe(
            'iReporter Contact'
        );
    });
});

describe('Testing the Title in the Landing Page', () => {
    test('assert that <title> is correct', async () => {
        await page.goto(INDEX);
        const title = await page.title();
        expect(title).toBe(
            'iReporter'
        );
    });
});

describe('Testing the Title in About Page', () => {
    test('assert that <title> is correct', async () => {
        await page.goto(ABOUT);
        const title = await page.title();
        expect(title).toBe(
            'iReporter About'
        );
    });
});

describe('Testing the Navbar exists', () => {
    test('assert that a div named navbar exists', async () => {
        await page.goto(SIGNUP);
        const navbar = await page.$eval('.navbar', el => (el ? true : false));
        expect(navbar).toBe(true);
      });
});
