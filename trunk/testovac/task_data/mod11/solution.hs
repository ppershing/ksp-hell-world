main :: IO()
main = do
	s <- getLine
	putStrLn (show (mod (foldl (\acc x -> (x-acc)) 0 [read [c]::Int | c<-s ]) 11 == 0))
