function logout(){
    document.cookie = "token=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;";
    document.cookie = "name=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;";
    document.cookie = "email=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;";
    document.cookie = "username=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;";
    document.cookie = "isAdmin=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;";
    document.cookie ="isLoggedIn=False;path=/;sameSite=Strict";
    window.location.replace("signin.html");
  
}