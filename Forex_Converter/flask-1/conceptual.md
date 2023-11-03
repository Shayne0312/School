Sure! Here are the answers to the questions using Markdown:

- **What are important differences between Python and JavaScript?**
  - Python:
    - is a scripting language
    - is used for backend development
    - is used for web development, data analysis, scientific computing, artificial intelligence, and more
  - JavaScript:
    - is a programming language
    - is used for frontend development
    - is primarily used for web development and is commonly used to add interactivity and dynamic behavior to websites

- **Given a dictionary like  `{"a": 1, "b": 2}` , list two ways you can try to get a missing key (like "c") *without* your programming crashing.**
dict = {"a": 1, "b": 2}
  value = dict.get("c")
  print(value)
- **What is a unit test?**
  - A unit test is a way of testing a specific unit - the smallest piece of code that can be logically isolated in a system. In most programming languages, that is a function, a subroutine, a method, or property.

- **What is an integration test?**
  - An integration test is a level of software testing where individual units are combined and tested as a group. The purpose of this level of testing is to expose faults in the interaction between integrated units or programs.

- **What is the role of a web application framework, like Flask?**
  - A web application framework is a software framework designed to aid and alleviate some of the headache involved in the development of web applications and services. Key features include user account management, routing, database abstraction, and templating.

- **You can pass information to Flask either as a parameter in a route URL (like '/foods/pretzel') or using a URL query param (like 'foods?type=pretzel'). How might you choose which one is a better fit for an application?**
  - Route URL is generally a better fit when the information being passed is essential to the resource being accessed, while using a URL query parameter is more suitable for optional or non-essential information. For example, if you were accessing a specific user's profile page, you would use a route URL to pass the user's ID, but if you were searching for a user by name, you would use a URL query parameter.

- **How do you collect data from a URL placeholder parameter using Flask?**
from flask import Flask
  app = Flask(__name__)

  @app.route('/users/<username>')
  def get_user(username):
      return f"User: {username}"

  if __name__ == '__main__':
      app.run()
- **How do you collect data from the query string using Flask?**
from flask import Flask, request
  app = Flask(__name__)

  @app.route('/search')
  def search():
      query = request.args.get('q')  # Access the value of the 'q' parameter
      return f"Search query: {query}"

  if __name__ == '__main__':
      app.run()
- **How do you collect data from the body of the request using Flask?**
from flask import Flask, request
  app = Flask(__name__)

  @app.route('/login', methods=['POST'])
  def login():
      username = request.form.get('username')
      password = request.form.get('password')
      # Rest of the login code
      return "Login successful"

  if __name__ == '__main__':
      app.run()
- **What is a cookie and what kinds of things are they commonly used for?**
  - A cookie is a type of metadata that is stored in a user's computer. Cookies are commonly used to store information about a user on a website so that the website can remember the user's preferences or login information. Essentially, it gives statefulness to the stateless HTTP protocol.

- **What is the session object in Flask?**
  - The session object is a dictionary that stores data across requests. It is used to store user information so that the user can access the website without having to log in every time they visit a new page.

- **What does Flask's  `jsonify()`  do?**
  - Flask's  `jsonify()`  converts a Python dictionary into a JSON object.