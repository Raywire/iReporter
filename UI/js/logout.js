function logout(){
    document.cookie = "token=;expires=Thu, 01 Jan 1970 00:00:01 GMT;";
    document.cookie = "name=;expires=Thu, 01 Jan 1970 00:00:01 GMT;";
    document.cookie = "email=;expires=Thu, 01 Jan 1970 00:00:01 GMT;";
    document.cookie = "username=;expires=Thu, 01 Jan 1970 00:00:01 GMT;";
    window.location.replace("signin.html");
  
}