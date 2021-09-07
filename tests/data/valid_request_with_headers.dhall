let Request = ./request.dhall

in    { variables = [] : List Text
      , method = Request.Method.POST
      , path = "x/foo/bar"
      , headers =
        [ Request.makeHeader "x-header-1" "value-1"
        , Request.makeHeader "x-header-2" "value-2"
        ]
      , body = "a request body"
      }
    : Request.Request
