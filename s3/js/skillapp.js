/*useful functions for stuff.  to be moved to script later*/
function getSkillList() {

  return $.ajax({
    type: "GET",
    url: "https://schema-management.cromulent-crm.com/",
    crossDomain: true,
    contentType: "application/json",
    headers: {
      "Authorization": get_auth_token()
    },
    dataType: "json"
  });

}

function getSkillSchema(skill) {

  return $.ajax({
    type: "GET",
    url: "https://schema-management.cromulent-crm.com/" + skill,
    crossDomain: true,
    contentType: "application/json",
    headers: {
      "Authorization": get_auth_token()
    },
    dataType: "json"
  });

}

function getSkills(skill) {

  return $.ajax({
    type: "GET",
    url: "https://record-services.cromulent-crm.com/" + skill,
    crossDomain: true,
    contentType: "application/json",
    headers: {
      "Authorization": get_auth_token()
    },
    dataType: "json"
  });

}

function getSkill(skill, guid) {

  return $.ajax({
    type: "GET",
    url: "https://record-services.cromulent-crm.com/" + skill + "/" + guid,
    crossDomain: true,
    contentType: "application/json",
    headers: {
      "Authorization": get_auth_token()
    },
    dataType: "json"
  });

}

function saveSkill(skill, data, guid) {

  theUrl = "https://record-services.cromulent-crm.com/" + skill;
  if (guid) {
    theUrl += "/" + guid;
  }

  return $.ajax({
    type: "PUT",
    url: theUrl,
    crossDomain: true,
    contentType: "application/json",
    headers: {
      "Authorization": get_auth_token()
    },
    dataType: "json",
    data: JSON.stringify(data),
    error: function (xhr, ajaxOptions, thrownError) {
        message = xhr.statusText + ": " + xhr.responseJSON.error;
        alert("An error occured processing the request.\n" + message);
      }
  });

}

function putCheckedSkills(skill, user_id, data) {

  return $.ajax({
    type: "PUT",
    url: "https://user-management.cromulent-crm.com/" + user_id + "/" + skill,
    crossDomain: true,
    contentType: "application/json",
    headers: {
      "Authorization": get_auth_token()
    },
    dataType: "json",
    data: JSON.stringify(data),
    error: function (xhr, ajaxOptions, thrownError) {
        message = xhr.statusText + ": " + xhr.responseJSON.error;
        alert("An error occured when saving skills.\n" + message);
      }
  });

}

function getCheckedSkills(skill,user_id) {

  return $.ajax({
    type: "GET",
    url: "https://user-management.cromulent-crm.com/" + user_id + "/" + skill,
    crossDomain: true,
    contentType: "application/json",
    headers: {
      "Authorization": get_auth_token()
    },
    dataType: "json"
  });


}

function deleteSkill(skill, guid) {
  return $.ajax({
    type: "DELETE",
    url: "https://record-services.cromulent-crm.com/" + skill + "/" + guid,
    crossDomain: true,
    contentType: "application/json",
    headers: {
      "Authorization": get_auth_token()
    },
    dataType: "json"
  });

}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function getUrlParameter(name) {
  name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
  var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
  var results = regex.exec(location.search);
  return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
};

function previewFile() {
  var preview = document.querySelector('img');
  var file = document.querySelector('input[type=file]').files[0];
  var reader = new FileReader();

  reader.addEventListener("load", function() {
    preview.src = reader.result;
  }, false);

  if (file) {
    reader.readAsDataURL(file);
  }
}
