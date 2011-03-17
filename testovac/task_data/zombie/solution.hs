main :: IO()
main = do
	s <- getLine
	if s == "srnka" then putStrLn "ano" else putStrLn "nie"
