# csbproject
LINK: https://github.com/simkatti/csbproject

This is a final course project for Helsinki University Cyber Security Base 1. This is a messenger application where you can create a user, you can sign in, send messages to other users (or yourself) and search and delete messages that have been sent to you. So essentially, a mix between an email and messaging app.

The app contains 6 security flaws from OWASP Top Ten 2017 list. The flaws are installed into the code and the fixes are commented out. This application can be run locally but with the security flaws it is very vulnerable. 

Installation instructions: Clone the git repo to a folder of your choice. Write a secret key in .env file or navigate to settings.py and change the secret key there. The application assumes your secret key is in .env file. Run migrations: python3 manage.py migrate
Run the app: python3 manage.py runserver
The database doesn’t have any users, so you start the testing by creating an account. 

FLAW 1: Broken Access Control
link: https://github.com/simkatti/csbproject/blob/main/messenger/views.py#L65
Description: Broken Access Control in deleteView function in views.py file. The deleteView function doesn’t authenticate the user before deleting the message, so that only the message reciever can delete it. This means that anyone who knows the message id or iterates through them can delete the message.
How to test the issue: Test the app and send messages to other users you have created or yourself. Find the message id from the browsers inspection tools. Log in as another user. Send a message to yourself and change the message id in the inspections tools, to the other users message id. Delete other users message by pressing the delete button. The user who is currently logged in should still see their own message. 
Fixing the issue: This issue is fixed with requesting the user and making sure that the users id matches the message id and only then the message can be deleted. The fix is commented out on lines 65, 66 and 68. 

FLAW 2: Cross Site Scripting
link: https://github.com/simkatti/csbproject/blob/main/messenger/views.py#L52
Description: Cross Site Scripting (XSS) vulnerability in views.py line 52. This allows other users to send messages with malicious content. 
How to test the issue: Log in to your account and send a message to yourself containing, for example, “<script>alert('hello')</script>”. When you go back on the home page there will be a JavaScript pop-up alert box. 
Fixing the issue: This issue is easily fixed by removing the mark_safe function. To make the content vulnerable for XXS attacks, I had to add mark_safe function in to the code. This is because by default in Django every template automatically escapes the output of every variable[1,2], making it safe for XXS attacks. The fix is commented on line 54.

FLAW 3: Sensitive Data Exposure
link: https://github.com/simkatti/csbproject/blob/main/messenger/views.py#L47
Description: There is a risk of sensitive data exposure in the homePage function in views.py file. All user received private messages are displayed on the homepage after the user has logged in. If the user logs out and goes back via the browsers back button, all the messages are there on display even if user is logged out. This happens because the messages are cached by the browser. 
How to test the issue: Log into your account and log out. Go back by clicking the browsers back button. You should see the homepage as if you were still logged in. 
Fixing the issue: The issue can be fixed by importing never_cache from django.views.decorators.cache and adding @never_cache decoration on top of the homePage fucntion. The commented out fix can be found on line 47 in the views.py. The import is not commented out in views.py.

FLAW 4: SQL Injection
link: https://github.com/simkatti/csbproject/blob/main/messenger/views.py#L98
Description: SQL injection vulnerability in views.py on line 98. This allows users to inject malicious SQL queries when using the search function. 
How to test the issue: Log into your account. Make sure there is some messages in the database. Use the search bar and type, for example, “ ‘ UNION SELECT * FROM messenger_message --”. This will show all the messages in the databse (it also makes an sensitive data exposure issue). 
Fixing the issue: The SQL injection issue can be fixed using Djangos objects when retrieving data from the database instead of SQL inquiries. The fix is on line 107 in the views.py file. 

FLAW 5: Security Misconfiguration
link: https://github.com/simkatti/csbproject/blob/main/myapp/settings.py#L33
Description: Security Misconfiguration issue in the settings.py on line 27. Debug is left True when it should be False. This allows the user to see detailed debbuging pages instead browsers plain error messages. 
Fixing the issue: Simply turning the debug to False. Fix is commented on line 28 in settings.py file. 

FLAW 6: Cross-site Request Forgery CSRF
link: https://github.com/simkatti/csbproject/blob/main/messenger/views.py#L48
Description: homePage function is made vulnerable for CSRF attacks by using the csrf_extempt function. This is a bonus flaw and in reality it would make no sense to use it. csrf_extempt function ignores the csrf protection on the home page making an attack possible. The user who is logged in can be forced to execute unwanted actions on the application [3].
Fixing the issue: Simply remove csrf_extempt on line 48 in views.py

Sources: 
[1] https://docs.djangoproject.com/en/5.0/topics/security/
[2] https://docs.djangoproject.com/en/5.0/ref/templates/language/#automatic-html-escaping
[3] https://owasp.org/www-community/attacks/csrf
