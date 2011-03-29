import List

main :: IO()
main = do
	s <- getLine
	putChar $ snd (maximum [(length (elemIndices c s), c) | c<-s ])
	putStrLn ""
