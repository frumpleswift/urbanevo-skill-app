/* authentication functions for the skill app */

/*after login
http://localhost:8080/#access_token=eyJraWQiOiI5aUdBeFB6WmxrWGNibDFubDkxbTE4VGdUWm5HalwvQ1ZFUTF3Zk1LaUFDdz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJlMGIxMzllOC1iMGZmLTRiZWQtYjQ1My03MTMyZWViNWNlZjUiLCJldmVudF9pZCI6ImM3OGMwZGQyLWEyMmItNDFlZS04YTZiLTZlYmFiYjI2ODM5OSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1NjM2MzUwMzUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX28wcjhGYWgxTyIsImV4cCI6MTU2MzYzODYzNSwiaWF0IjoxNTYzNjM1MDM1LCJ2ZXJzaW9uIjoyLCJqdGkiOiIwOWRkOTE0MS00MjFkLTQ5YWQtYjc1My1iMzQ0YmM5NDA0MWQiLCJjbGllbnRfaWQiOiI3cWJkcHU3M3AzZzdwdHE0bG40N25zZWlmcCIsInVzZXJuYW1lIjoiZnJ1bXBsZXN3aWZ0In0.b6qnxTTtNAlTwDTyj_n7GjQRDMg2xDDckyT0-k5Q5yQnNhxKkMCoHlhZDTAFtATHj-cc_rXahVJ9wqs7y5ijrPT6gWl3dsH66mJXSSKDozjc6r_yVw2R5ZVOXBNj8q5z2HPW2rqBTasmswDVPAXUSCndDwNQAi-0pfvvIFASDS1ruQBlNvnb_0VfsxrodBIKnJO84kUaQimwPOR2fUIHqk-ko2JVA2Ry_raWzJG2z2R6a9rjNYGG7XxjW6CSxgSl0ubrb8VgtEqIY1RUaowN0tiCF7k-mHTK7kDplQGKEnEg4hB74tnL9xrvqwDvXitTWDX-ZeOA9lABd-WuVIXIeA&expires_in=3600&token_type=Bearer

eyJraWQiOiI5aUdBeFB6WmxrWGNibDFubDkxbTE4VGdUWm5HalwvQ1ZFUTF3Zk1LaUFDdz0iLCJhbGciOiJSUzI1NiJ9
eyJzdWIiOiJlMGIxMzllOC1iMGZmLTRiZWQtYjQ1My03MTMyZWViNWNlZjUiLCJldmVudF9pZCI6ImM3OGMwZGQyLWEyMmItNDFlZS04YTZiLTZlYmFiYjI2ODM5OSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1NjM2MzUwMzUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX28wcjhGYWgxTyIsImV4cCI6MTU2MzYzODYzNSwiaWF0IjoxNTYzNjM1MDM1LCJ2ZXJzaW9uIjoyLCJqdGkiOiIwOWRkOTE0MS00MjFkLTQ5YWQtYjc1My1iMzQ0YmM5NDA0MWQiLCJjbGllbnRfaWQiOiI3cWJkcHU3M3AzZzdwdHE0bG40N25zZWlmcCIsInVzZXJuYW1lIjoiZnJ1bXBsZXN3aWZ0In0
b6qnxTTtNAlTwDTyj_n7GjQRDMg2xDDckyT0-k5Q5yQnNhxKkMCoHlhZDTAFtATHj-cc_rXahVJ9wqs7y5ijrPT6gWl3dsH66mJXSSKDozjc6r_yVw2R5ZVOXBNj8q5z2HPW2rqBTasmswDVPAXUSCndDwNQAi-0pfvvIFASDS1ruQBlNvnb_0VfsxrodBIKnJO84kUaQimwPOR2fUIHqk-ko2JVA2Ry_raWzJG2z2R6a9rjNYGG7XxjW6CSxgSl0ubrb8VgtEqIY1RUaowN0tiCF7k-mHTK7kDplQGKEnEg4hB74tnL9xrvqwDvXitTWDX-ZeOA9lABd-WuVIXIeA

https://accounts.google.com/signin/oauth/oauthchooseaccount?client_id=626426903548-8j89d5638db7kl6gngmoahsn6eoll85m.apps.googleusercontent.com&as=C8iCXkFIK8nM0LbmF5fwbA&destination=https%3A%2F%2Fauth.cromulent-crm.com&approval_state=!ChRWWFljTjBGbUhxOGpCU2U5UHp0RBIfVTgyUlQxTjVFM0VTVUU3MWpGWk5XazBEbk40YXdSWQ%E2%88%99AJDr988AAAAAXTTywb_FUyxJZNMujfnt0l-D1Ys-aPdu&oauthgdpr=1&xsrfsig=ChkAeAh8T5GK-1CpKMePSCW-6tIYGXEphIZJEg5hcHByb3ZhbF9zdGF0ZRILZGVzdGluYXRpb24SBXNvYWN1Eg9vYXV0aHJpc2t5c2NvcGU&flowName=GeneralOAuthFlow

https://accounts.google.com/signin/oauth/consent?authuser=0&part=AJi8hANdwsfPImGyMc5-WG6ozMNFkMbnJJbF21Dq0gUTx9ZAMjFPu59lzGXy1AUGeWM7S3IPKRrXw0lCiGWrIS9n3l6RY3lTBovFtMjLqUHiLN3u5n7BnkVq6Hc0cFUmXlAzY4xif3zTETMlnzweF_r84pSqeEeotgSxl5nr0EytpZ4NefwNIsa5A4bI7uBeNLjgpleg2Av1zvINUYN9zguQhU5zPV78TXdqvT8nZBXtyBqvm5aAzWI9RNSctYwIVVgyeOEj8M9-CuWKf4M0AuD6hD-vtOBGQ1Zj2dcmX-PcHNIxM0T5B_f_LbUrMU2mrlExBjht0LHHTB0ODWWywwBbH-qgtPcKVbuSZJGXKVGGMvjLvpvXOCk3l34qKC9XAtn1CMLMSaTTs3jB2cKdLzSU06bW1qqwT3SU6nmNZOurYJU-SUCrUzBj5tO4AN_cnneNOS6vojqu&as=RMjWoYriQbgjPl3KxrnjzA&pli=1&rapt=AEjHL4OX4B3mb_MZDG8Z4vHdZOPcZeU5Ya0FMJvnxqMOHobQYsfdaBKcmSkMsvOsh-75vtZSAqO232GtPMqGHhgYRO7fqBsS_A&auth=mQfrYGHANVqKUuPAlA-jHhEbVDCmkYqD5vexZp5vD3MMNW8-V8g8dVHVzz0qTIp-eKH4ZA.

*/
/*reference urls
https://medium.com/@awskarthik82/part-1-securing-aws-api-gateway-using-aws-cognito-oauth2-scopes-410e7fb4a4c0
https://medium.com/@inishant/access-to-user-level-folders-using-amazon-s3-and-cognito-469e80dce4c6

for aws policy definitions
${cognito-identity.amazonaws.com:sub}

*/
//"https://auth.cromulent-crm.com/login?response_type=token&client_id=7qbdpu73p3g7ptq4ln47nseifp&redirect_uri=http://localhost:8080/"
auth_url="https://auth.cromulent-crm.com"
response_type="token"
client_id="7qbdpu73p3g7ptq4ln47nseifp"
redirect_uri=document.location.protocol + "//" + document.location.hostname;
if (document.location.port) {
  redirect_uri = redirect_uri + ":" + document.location.port;
}
redirect_uri += "/";

auth_link=auth_url+"/login?response_type="+response_type+"&client_id="+client_id+"&redirect_uri="+redirect_uri;
logout_link=auth_url+"/logout?response_type="+response_type+"&client_id="+client_id+"&redirect_uri="+redirect_uri;

console.log(document.cookie);

function get_auth_token() {

  try {
    try {
      query_token = document.location.toString().match(/\#(?:access_token)\=([\S\s]*?)\&/)[1];
    } catch(err) {
      query_token = document.location.toString().match(/\#(?:id_token)\=([\S\s]*?)\&/)[1];
    }
    console.log("Setting access_token: " + query_token)
    document.cookie = "access_token=" +query_token+";";

  } catch(err) { /* don't care if not set */ }

  token = getCookie("access_token")
  return token;
}

//check if the JWT authorizes admin access
//ths is for gui display purposes Only
//RBAC controls are enforced on the API backend
function is_admin() {

  try {
    token = get_auth_token();
    payload = window.atob( token.split(".")[1]);
    groups = JSON.parse(payload)["cognito:groups"];
    ret = groups.includes("SkillApp-Cognito-Admin-Group");

  } catch(err) {
    ret = false;
    console.log(err);
  }

  return ret;

}

function get_user_id() {

  token = get_auth_token();
  payload = window.atob( token.split(".")[1]);
  user_id = JSON.parse(payload)["sub"];
  console.log("User ID: " + user_id);
  return user_id;

}

function logout_steps() {
  document.cookie = "access_token=;"
}


// Set the authToken //
get_auth_token();


if (get_auth_token()) {
  $(document).ready(function() {
    //there is a logged on user
    $("#loginlink").text("Logout");
    $("#loginlink").attr("href",logout_link);
    $("#loginlink").click(logout_steps);
  });
} else {
  $(document).ready(function() {
    $("#loginlink").off("click");
    $("#loginlink").attr("href",auth_link);
  });
}
