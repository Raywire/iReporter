describe('Testing the functionality, convert utc to local time', () => {
  it('should convert utc to Kenyan Time', () => {
    let utcTime = "Sun, 13 Jan 2019 20:36:27 GMT"

    expect(convertToLocalTime(utcTime)).toBe("Sun, Jan 13th 2019, 11:36:27 pm +03:00");
  })
})

describe('Testing the functionality, to get a cookie', () => {
  it('should check if a cookie exists', () => {
    document.cookie = "username=John Doe";

    expect(getCookie("username")).toBe("John Doe");
  })
})

describe('Testing the functionality, to check if cookies are reset on logout', () => {
  it('should check if cookies are cleared on logout', () => {
    document.cookie = "username=;expires=Thu, 01 Jan 1970 00:00:01 GMT;";

    expect(getCookie("username")).toBe("");
  })
})