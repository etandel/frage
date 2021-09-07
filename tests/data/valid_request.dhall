let Request = ./request.dhall

let req
    : Request.Request
    = { method = Request.Method.POST
      , path = "/x/foo/bar"
      , headers = {=}
      , body = "a request body"
      }

in  req
