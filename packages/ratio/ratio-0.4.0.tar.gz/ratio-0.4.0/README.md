<h1 align="center">Ratio</h1>
<p align="center">
  The Python web framework for developers who want to get shit done.
</p>

---

**Ratio is currently being developed and all releases in this phase may introduce breaking changes until further notice.
Please do not use Ratio in production without carefully considering the consequences.**

---

## What is Ratio?
Ratio is an asynchronous Python web framework that was built with developer experience in mind. Quick to learn for those
who just start out with programming and powerful so that senior developers can build high performance web applications 
with it. The framework is designed with the Goldilocks principle in mind: just enough. Enough power to run high performance
web applications, enough intuitive design, so that developers can easily pick up on the principles.

Ratio borrows ideas from great frameworks, like [Django](https://github.com/django/django), [FastAPI](https://github.com/tiangolo/fastapi)
and [Next.js](https://github.com/vercel/next.js). It combines those ideas with original concepts to improve the life of 
a developer when building web applications for any purpose.

## Ready out of the box 
Ratio will be shipped with a custom and extensible command line interface, which can be used to perform actions within a
project.
  
This is what we aim Ratio to do:

- **File based routing:** Intuitive routing for each incoming request, based on file system.
- **Integrates with databases:** Connect to SQL or SQLite databases from within the application controllers.
- **Write once, use everywhere:** Do not repeat yourself, by defining models, routes and actions you can use them throughout the application.
- **Adheres to standards:** API views are based on [OpenAPI]() and the [JSON schema standard]().

_This list is not complete and will be extended after certain releases in the pre-release phase._


## Minimal external dependencies
Currently, Ratio only requires the `rich` package from outside the Python standard library, which is used 
for rendering beautiful output to the command line. In a future version of Ratio, we might want to remove this direct
dependency for users who really want to have no external dependencies.
