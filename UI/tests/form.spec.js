import faker from "faker";
import puppeteer from "puppeteer";

const appUrlBase = 'http://localhost:8000';
const SIGNIN = `${appUrlBase}/signin.html`;
const SIGNUP = `${appUrlBase}/signup.html`;
const RESET_REQUEST = `${appUrlBase}/reset_request.html`;
const RESET_PASSWORD = `${appUrlBase}/reset_password.html`;
const CONTACT = `${appUrlBase}/contact.html`;

const lead = {
  firstname: faker.name.firstName(),
  lastname: faker.name.lastName(),
  fullname: `${faker.name.firstName()} ${faker.name.lastName()}`,
  username: 'johndoe',
  email: faker.internet.email(),
  password: '123456',
  confirm_password: '123456',
  message: faker.random.words()
};

let page;
let browser;
const width = 1280;
const height = 720;

beforeAll(async () => {
  browser = await puppeteer.launch({

  });
  page = await browser.newPage();
});
afterAll(() => {
  browser.close();
});

describe("Sign Up form", () => {
  test("user can sign up", async () => {
    await page.goto(SIGNUP);
    await page.waitForSelector("[id=signUp]");
    await page.click("input[name=firstname]");
    await page.type("input[name=firstname]", lead.firstname);
    await page.click("input[name=lastname]");
    await page.type("input[name=lastname]", lead.lastname);
    await page.click("input[name=username]");
    await page.type("input[name=username]", lead.username);
    await page.click("input[name=email]");
    await page.type("input[name=email]", lead.email);
    await page.click("input[name=password]");
    await page.type("input[name=password]", lead.password);
    await page.click("input[name=confirm_password]");
    await page.type("input[name=confirm_password]", lead.confirm_password);
    await page.click("input[type=submit]");
  }, 26000);
});

describe("Sign In form", () => {
  test("user can sign in to the app", async () => {
    await page.goto(SIGNIN);
    await page.waitForSelector("[id=signIn]");
    await page.click("input[name=username]");
    await page.type("input[name=username]", lead.email);
    await page.click("input[name=password]");
    await page.type("input[name=password]", lead.password);
    await page.click("input[type=submit]");
  }, 16000);
});

describe("Request Password reset form", () => {
  test("user can request for a password reset", async () => {
    await page.goto(RESET_REQUEST);
    await page.waitForSelector("[id=requestReset]");
    await page.click("input[name=name]");
    await page.type("input[name=name]", lead.username);
    await page.click("input[type=submit]");
  }, 16000);
});

describe("Contact form", () => {
  test("user can submit a contact request", async () => {
    await page.goto(CONTACT);
    await page.waitForSelector("[id=postMessage]");
    await page.click("input[name=name]");
    await page.type("input[name=name]", lead.fullname);
    await page.click("textarea[name=comment]");
    await page.type("textarea[name=comment]", lead.message);
    await page.click("input[type=submit]");
  }, 16000);
});

describe("Reset Password form", () => {
  test("user can reset password", async () => {
    await page.goto(RESET_PASSWORD);
    await page.waitForSelector("[id=resetPassword]");
    await page.click("input[name=password]");
    await page.type("input[name=password]", lead.password);
    await page.click("input[name=confirm_password]");
    await page.type("input[name=confirm_password]", lead.confirm_password);
    await page.click("input[type=submit]");
  }, 26000);
});