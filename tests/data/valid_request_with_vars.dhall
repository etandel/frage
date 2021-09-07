let Request = ./request.dhall

in    { variables = [ "var1", "var2" ]
      , method = Request.Method.POST
      , path = "x/foo/bar"
      , headers = [] : Request.Headers
      , body = "a request body with var1 = {var1} and var2 = {var2}"
      }
    : Request.Request
