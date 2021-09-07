let Method = < HEAD | OPTIONS | GET | POST | PUT | PATCH | DELETE | TRACE | CONNECT >

let Url = Text
let Headers = {}
let Body = Text


let Request = {
  method : Method,
  path: Url,
  headers: Headers,
  body: Body,
}

in 

{
  Request = Request,
  Method = Method,
  Url = Url,
  Headers = Headers,
  Body = Body,
}
