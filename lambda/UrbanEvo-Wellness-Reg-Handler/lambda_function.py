import json

import re
import os
from botocore.vendored import requests
import traceback
import hashlib
import boto3
import datetime
import os
import io
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
from botocore.exceptions import ClientError
from lxml import html


# code to simulate wellness html interaction
def userlogin(password, email):

    # start a session by pulling up the login page
    session = requests.Session()
    r = session.get(
        'https://www.wellnessliving.com/login/urbanevo', timeout=30)

    # need to get the csrf from the reply
    # "a_form_csrf['core-request-api']='0TC8QbYNvdCYYOTj-VVnPqhcQwD8'"
    csrfPos = [m.start() for m in re.finditer(
        "a_form_csrf\[\'core-request-api\'\]\=\'", r.text)]
    csrf = r.text[csrfPos[0]:csrfPos[0] + 63][33:61]

    # retrieve a salt from the salt service
    # notepadPost={"s_login":email,"s_type":"","csrf":"0TC8QbYNvdCYYOTj-VVnPqhcQwD8","_":"1538843048758"}
    notepad = session.get('https://www.wellnessliving.com/Core/Passport/Login/Enter/Notepad.json?s_login=' +
                          email + '&s_type=&csrf=' + csrf + '&_=1538843048758')
    notepadData = notepad.json()
    salt = notepadData["s_notepad"]

    # this is a copy from the wellness js that handles the "passport" processself.
    # i believe this is the hashing mechanism used on the server side to store password
    s_hash = ''
    delim = ['r', '4S', 'zqX', 'zqiOK', 'TLVS75V', 'Ue5aLaIIG75',
             'uODJYM2JsCX4G', 'kt58wZfHHGQkHW4QN', 'Lh9Fl5989crMU4E7P6E']
    for a in delim:
        s_hash = s_hash + a + password

    firstHash = salt + hashlib.sha3_512(s_hash.encode('utf-8')).hexdigest()

    secondHash = hashlib.sha3_512(firstHash.encode('utf-8')).hexdigest()

    loginData = {'i': 0, 's_password': secondHash, 's_login': email, 's_notepad': notepadData["s_notepad"], 's_captcha': '', 'csrf': csrf
                 }

    loginResponse = session.post(
        "https://www.wellnessliving.com/Core/Passport/Login/Enter/Enter.json", data=loginData)
    print(loginResponse)
    # need to get the UiD
    userInfoGet = session.get(
        "https://www.wellnessliving.com/Core/Passport/Login/Info.json?csrf=" + csrf + "&_=1538843048759")
    print(userInfoGet)
    userInfo = userInfoGet.json()
    print(userInfo)
    # getuserinfo=session.get("https://www.wellnessliving.com//rs/schedule/urbanevo?k_class_tab=2868&uid=12314053&id_class_tab=1")
    print( {"session": session, "uid": userInfo["uid"], "csrf": csrf} )
    return {"session": session, "uid": userInfo["uid"], "csrf": csrf}


def verifyEmail(email):

    session = requests.Session()
    r = session.get(
        'https://www.wellnessliving.com/selfsignup/37RrPjmtY', timeout=5)

    tree = html.fromstring(r.text.replace('\\', ''))

    controller = tree.xpath("//script[contains(.,'Ajax._startup')]/text()")
    ajaxID = str(controller[0]).split("'")[1]

    emailData = {'a-ajax': ajaxID, 'a_data[id_place]': '4', 'a_data[s_mail]': email, 'a_data[uid_current]': 0, 'a_data[s_secret]': '37RrPjmtY', 's_method': 'Wl\Login\Add\Ajax::mailVerifyPrompt'
                 }

    r = session.post("https://www.wellnessliving.com/a/ajax.html",
                     data=emailData, timeout=10)

    print("In verify: {}".format(r.text))

    return r.text


def createUser(fname, lname, email, pwd, phone, phoneHome, phoneWork, month, day, year, gender, address, city, postal, location, signature, city_code=27495):

    session = requests.Session()
    r = session.get(
        'https://www.wellnessliving.com/Wl/Selfsignup.html?a-ajax=1&id_page=1&s_secret=37RrPjmtY&uid=0&a-ajax=1&_=1516447931224', timeout=15)
    tree = html.fromstring(r.text.replace('\\', ''))
    postURL = tree.xpath('//form/@action')
    print("Action URL: {}".format(postURL))
    controller = tree.xpath(
            '//input[@name="wl-selfsignup-controller"]/@value')
    print("Controller: {}".format(controller))
    userData = {'wl-selfsignup-controller': controller[0], 's_secret': '37RrPjmtY', 'a_image_upload[PassportLoginImage-new]': '', 'is_more': 1, 's_firstname': fname, 's_lastname': lname, 'a_user[not_virtual]': 1, 'a_user[s_mail]': email, 'a_user[is_password_new]': 1, 'a_user[s_password]': pwd, 'a_user[s_password2]': pwd, 's_phone': phone, 's_phone_home': phoneHome, 's_phone_work': phoneWork, 'i_month': month, 'i_day': day, 'i_year': year, 'id_gender': int(gender), 'is_address_inherit': '', 's_address': address, 's_city_custom': city, 'k_city': city_code  # 27495 #code returned by the city search plugin?
                    , 's_postal': postal, 'k_location': location  # 208833 #sterling v alexandria??
                    , 's_search': '', 'uid_referrer': 0, 'a-ajax': 1
                    }
    print("User Data: {}".format(userData))
    r = session.post(postURL[0], data=userData, timeout=45)
    print ("Signup Response: {}".format(r.text))
    tree = html.fromstring(r.text.replace('\\', ''))
    if "\"s_status\":\"post-error\"" in r.text:
        raise Exception("An error occured while creating the User")
    postURL = tree.xpath('//form/@action')
    controller = tree.xpath('//input[@name="wl-selfsignup-controller"]/@value')
    print("Action URL: {}".format(postURL))
    print("Controller: {}".format(controller))
    affirmData = {'wl-selfsignup-controller': controller[0], 'is_agree': 1, 's_signature': signature, 'a-ajax': 1}
    print("Affirm Data: {}".format(affirmData))
    print("Sanity Check")
    r = session.post(postURL[0], data=affirmData, timeout=45)
    print("Affirm Response: {}".format(r.text))
    return r.text

def addMember(fname, lname, email, pwd, phone, phoneHome, phoneWork, month, day, year, gender, address, city, postal, location, signature, city_code=27495, attempt=1):

    try:

        session = userlogin(pwd, email)

        print("Session: ".format(session))
        addProfileURL = 'https://www.wellnessliving.com/rs/profile-edit.html?uid_from=' + session["uid"]

    # Add Profile:
    # Request:
        # print(session["session"].get(addProfileURL))
        r = session["session"].get(addProfileURL)

        # print ("Click add profile")
        # print (r.text)

        tree = html.fromstring(r.text.replace('\\', ''))
        postURL = tree.xpath('//form/@action')
        controller = tree.xpath('//input[@name="rs-profile-edit"]/@value')

    # Edit Profile:
        addData = {"rs-profile-edit": controller[0], "a_pay[uid]": 0, "a_family_relation[0][id_family_relation]": 5, "a_family_relation[0][uid_to]": session["uid"], "a_image_upload[PassportLoginImage-new]": "", "is_more": 1, "s_firstname": fname, "s_lastname": lname, "a_user[is_mail_inherit]": "on", "a_user[is_password_new]": 1, "s_phone": phone, "s_phone_home": phoneHome, "s_phone_work": phoneWork, "i_month": month, "i_day": day, "i_year": year, "id_gender": gender, "s_address": address, "s_city_custom": city, "k_city": city_code  # 27495 #???where does this number come from?
                   , "s_postal": postal, "k_location": location  # 208833 #sterling??
                   , "s_search": '', "uid_referrer": 0
                   }

        # print("Child Data:")
        # print(addData)
        # print(postURL)

        r = session["session"].post(postURL[0], data=addData)

        # print (r.text)
        tree = html.fromstring(r.text.replace('\\', ''))
        links = tree.xpath(
            "//a[contains(@href,'relative-login') and contains(@title,'" + fname + "')]/@href")

        signInURL = links[0]
        addedUID = str(links[0]).split("=")[-1]

    # Sign Waiver:

    # "sign in" as the added user
        r = session["session"].get(signInURL)

#    print r.text
    # now get the waiver form for the new user
        r = session["session"].get(
            'https://www.wellnessliving.com/rs/login-agree.html', timeout=30)

#    print r.text
        try:
            tree = html.fromstring(r.text.replace('\\', ''))

            postURL = 'https://www.wellnessliving.com/a/ajax.html'

            controller = tree.xpath(
                "//script[contains(.,'Ajax._startup')]/text()")
            ajaxID = str(controller[0]).split("'")[1]

            affirmData = {'a-ajax': ajaxID, 'a_data[is_catalog_register]': 0, 'a_data[k_business]': 78906  # urbanevo number?
                          , 'a_data[s_signature]': signature, 's_method': 'RsLogin::agreeBusiness'
                          }

        except:

            print ("Error parsing add child request")
            print (r.text)
            raise

        r = session["session"].post(postURL, data=affirmData, timeout=60)

#    print r.text
        return r.text

    except Exception as e:
        print("An error occurred while adding a child on attempt {}".format(attempt))
        traceback.print_exc()
        if attempt <= 10:
            print("Retry creating child {} {} for {}".format(fname, lname, email))
            return addMember(fname, lname, email, pwd, phone, phoneHome, phoneWork, month, day, year, gender, address, city, postal, location, signature, city_code=27495, attempt=attempt + 1)
        print("Final attempt to create child failed")
        return {"error": "Error creating child: " + str(e)}

# end wellness skinning code

# data cleansing


def formatPhone(phone):

    print(phone)
    print(type(phone))

    if phone != "":

        reg = re.compile('\D')
        phone = reg.sub('', phone)
        phone = phone[0:3] + "-" + phone[3:6] + "-" + phone[6:]

    # print(phone)
    return phone

# lambda handler


def lambda_handler(event, context):
    #{"the_email": "g.o.l.d.e.n@tablets.com", "the_time": "1571786879", "the_other": "shitty"}
    message = json.loads(event['Records'][0]['Sns']['Message'])

    print(message)

    dynamodb = boto3.client('dynamodb')
    table_name = os.environ["WELLNESS_TABLE"]
    deserializer = TypeDeserializer()

    email = message["the_email"]
    crud_time = message["the_time"]
    password = message["the_other"]

    record = dynamodb.get_item(TableName=table_name,Key={"email":{"S":email},"crud_time":{"N":crud_time}})

    content = deserializer.deserialize(record.get('Item').get("user_data"))
    content["pwd"] = password

    print(content)

    # request info
    status = 200
    method = event.get('httpMethod')

    try:

        print ("Registering " + content["email"])
        phone = formatPhone(content["phone"])
        phoneHome = formatPhone(content.get("phoneHome",""))
        phoneWork = formatPhone(content.get("phoneWork",""))
        print(phone, phoneHome, phoneWork)
        checkEmail = verifyEmail(email)
        if "s_message" in checkEmail or "already" in checkEmail:

            raise Exception('Email Address Already Registered')

        else:
            print("Made it to user registration")
            userResult = createUser(content["fname"], content["lname"], content["email"], content["pwd"], phone, phoneHome, phoneWork, content["month"], content["day"],
                                    content["year"], content["gender"], content["address"], content["city"], content["postal"], content["location"], content["signature"], content["city_code"])
            print("User Added " + content["email"])
            memberResult = []
            for member in content["members"]:
                print("Adding Child")
                memberResult = memberResult + [addMember(member["fname"], member["lname"], content["email"], content["pwd"], phone, phoneHome, phoneWork, member["month"], member["day"],
                                                        member["year"], member["gender"], content["address"], content["city"], content["postal"], content["location"], content["signature"], content["city_code"])]
                print ("Child Added " + member["fname"])
            ret = {"UserResult": userResult, "DependentResults": memberResult}
    except Exception as e:
        raise

    print("Processing complete for {}".format(email))

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(ret)
    }
