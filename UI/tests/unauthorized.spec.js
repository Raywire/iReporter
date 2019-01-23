import puppeteer from "puppeteer";

const appUrlBase = 'https://raywire.github.io/iReporter/UI';
const HOME = `${appUrlBase}/home.html`;
const PROFILE = `${appUrlBase}/profile.html`;
const INTERVENTIONS = `${appUrlBase}/interventions.html`;
const REDFLAGS = `${appUrlBase}/redflags.html`;
const ADMIN = `${appUrlBase}/admin.html`;

let page;
let browser;

beforeAll(async () => {
  browser = await puppeteer.launch();
  page = await browser.newPage();
});
afterAll(() => {
  browser.close();
});

describe('Unathorized view in Dashboard', () => {
  test('users that are not logged in are redirected to sign in page', async () => {
    await page.goto(HOME);
    await page.waitForSelector('[id=signIn]')
  }, 9000000);
});

describe('Unathorized view in Profile Page', () => {
  test('users that are not logged in are redirected to sign in page', async () => {
    await page.goto(PROFILE);
    await page.waitForSelector('[id=signIn]')
  }, 9000000);
});

describe('Unathorized view in Interventions Page', () => {
  test('users that are not logged in are redirected to sign in page', async () => {
    await page.goto(INTERVENTIONS);
    await page.waitForSelector('[id=signIn]')
  }, 9000000);
});

describe('Unathorized view in Red-flags Page', () => {
  test('users that are not logged in are redirected to sign in page', async () => {
    await page.goto(REDFLAGS);
    await page.waitForSelector('[id=signIn]')
  }, 9000000);
});

describe('Unathorized view in Admin Page', () => {
  test('users that are not logged in are redirected to sign in page', async () => {
    await page.goto(ADMIN);
    await page.waitForSelector('[id=signIn]')
  }, 9000000);
});
