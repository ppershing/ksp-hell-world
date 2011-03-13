import List

main :: IO()
main = do
	n <- getLine
	s <- getLine
	putStrLn $ sort $ nub [c | c<-s, (length (elemIndices c s)) >= (read n::Int)]
