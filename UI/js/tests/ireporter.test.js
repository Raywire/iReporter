describe('Testing the functionality, convert utc to local time', () => {
  it('should convert utc to Kenyan Time', () => {
    let utcTime = "Sun, 13 Jan 2019 20:36:27 GMT"

    expect(convertToLocalTime(utcTime)).toBe("Sun, Jan 13th 2019, 11:36:27 pm +03:00");
  })
})

describe('Testing the functionality, to get a cookie', () => {
  it('should check if a cookie exists', () => {
    document.cookie = "testusername=John Doe";

    expect(getCookie("testusername")).toBe("John Doe");
  })
})

describe('Testing the functionality, to check if cookies are reset on logout', () => {
  it('should check if cookies are cleared on logout', () => {
    document.cookie = "testusername=;expires=Thu, 01 Jan 1970 00:00:01 GMT;";

    expect(getCookie("testusername")).toBe("logged out");
  })
})

describe('Testing the functionality, to check login feature', () => {
  it('should check if a user can access login', () => {
    let email = 'john@doe.com';
    let password = 'helloworld';

    expect(Users.exists(email, password)).toEqual(false);
    givenUserExists(email, password);
    expect(Users.exists(email, password)).toEqual(true);
  })
})