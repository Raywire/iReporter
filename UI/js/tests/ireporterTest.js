describe('Testing the functionality, convert utc to local time', ()=>{
    it('should convert utc to Kenyan Time', ()=>{
        let utcTime = "Sun, 13 Jan 2019 20:36:27 GMT"

      expect(convertToLocalTime(utcTime)).toBe("Sun, Jan 13th 2019, 11:36:27 pm +03:00");
    })
  })
  