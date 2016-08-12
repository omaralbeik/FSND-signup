#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import re
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):

    name = ""

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def validate_username(self, username):
        user_re = re.compile("^[a-zA-Z0-9_-]{3,20}$")
        return user_re.match(username)

    def validate_password(self, password):
        pass_re = re.compile("^.{3,20}$")
        return pass_re.match(password)

    def validate_email(self, email):
        email_re = re.compile("^[\S]+@[\S]+.[\S]+$")
        return email_re.match(email)


class MainPage(Handler):

    def get(self):
        self.render("signup.html")

    def post(self):
        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""
        success = False

        username = self.request.get("username")
        Handler.name = username
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if not self.validate_username(username):
            username_error = "That's not a valid username."

        if not self.validate_password(password):
            password_error = "That wasn't a valid password."

        if not password == verify:
            verify_error = "Your passwords didn't match."

        if email:
            if not self.validate_email(email):
                email_error = "That's not a valid email."

        if username_error == "" and password_error == "" and verify_error == "" and email_error == "":
            success = True

        if not success == True:
            self.render("signup.html",
                    username=username,
                    email=email,
                    username_error=username_error,
                    password_error=password_error,
                    verify_error=verify_error,
                    email_error=email_error)
        else:
            self.redirect("/success")

class SuccessPage(Handler):

    def get(self):
        self.render("success.html", name=self.name)

app = webapp2.WSGIApplication([('/', MainPage), ('/success', SuccessPage)], debug=True)
