let Map = https://prelude.dhall-lang.org/v15.0.0/Map/Type

let Method =
      < HEAD | OPTIONS | GET | POST | PUT | PATCH | DELETE | TRACE | CONNECT >

let Url = Text

let Headers = Map Text Text

let makeHeader = \(k : Text) -> \(v : Text) -> { mapKey = k, mapValue = v }

let Body = Text

let Request =
      { variables : List Text
      , method : Method
      , path : Url
      , headers : Headers
      , body : Body
      }

in  { Request, Method, Url, Headers, makeHeader, Body }
