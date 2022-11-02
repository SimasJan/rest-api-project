

**Branches:**
- `main`: contains all files, but no `tests/` folder.
- `testing-branch`: same as main, but including `tests/` folder.


----
Material taken from the course on Udemy (accessed on 27 October 2022):
https://ibm-learning.udemy.com/course/rest-api-flask-and-python/?src=sac&kw=python+api

E-book of the course:
https://rest-apis-flask.teclado.com/docs/course_intro/

Discord channel: https://discord.gg/78Nvd3p

In-depth docker tutorial:
https://rest-apis-flask.teclado.com/docs/docker_intro/in_depth_docker_tutorial/

---
### JWT

**Getting Access Token**

1. The client send authentication information to the API (usually, username and password)
2. The API validates them and generates an access token (in our case, a JWT)
3. Inside the JWT, the user's unique ID is stored.
4. The access token is sent back to the client for storage (i.e. cookie, other) and later use.

**[JWT encoder-decoder website](!https://jwt.io/)**


