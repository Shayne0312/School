### Conceptual Exercise

Answer the following questions below:

- What is RESTful routing?
- Representational State Transfer (REST) is a set of conventions for designing APIs.
- RESTful routing is a way to describe how a web server should respond to a client request in a predictable way to map HTTP methods (GET, POST, PUT, DELETE, etc.)


- What is a resource?
- RESOURCE: A resource is a representation of a specific data.

- When building a JSON API why do you not include routes to render a form that when submitted creates a new user?
- JSON APIs do not include routes to render forms because they follow a stateless approach and separate data representation from user interfacers.


- What does idempotent mean? Which HTTP verbs are idempotent?
- IDEMPODENT: Multiple identical request can be sent multiple times in a single request.
- VERBS: POST, PUT, DELETE, GET, PATCH, and PUT


- What is the difference between PUT and PATCH?
- PUT: The PUT method is used to completely replace an existing resource with a new representation provided in the request.
- PATCH: The PATCH method is used to replace an existing resource with a new representation provided in the request.

- What is one way encryption?
- One-way encryption, also known as hashing.

- What is the purpose of a `salt` when hashing a password?
- A salt is a randomly generated value that is combined with the password before hashing.

- What is the purpose of the Bcrypt module?
- Bcrypt is designed to be a slow and computationally intesive hashing algorithm.

- What is the difference between authorization and authentication?
- Authentication: Authentication is the process of verifying the identity of a user.
- Authorization: Authorization is the process of granting access to a resource.
- Example: Authentication checks to see if you are logged in, and authorization checks to see if you have access to a specific resource I.E. Admin/Mod/Dev perms or even specific routes.

