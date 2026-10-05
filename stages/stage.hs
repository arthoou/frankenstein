import Data.Char (isSpace)
import Data.List (dropWhileEnd)

main :: IO ()
main = do
  s <- getContents
  let t = dropWhileEnd isSpace (dropWhile isSpace s)
  putStr (t ++ " -> Haskell")
