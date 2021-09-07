let Request = ./request.dhall

in    { method = Request.Method.POST
      , path = "x/foo/bar"
      , headers = [] : Request.Headers
      , body = "a request body"
      }
    : Request.Request
