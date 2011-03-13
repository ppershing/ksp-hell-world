import List

main :: IO()
main = do
	input <- getLine
	let (n,b) = splitAt (head (elemIndices ' ' input)) input
	putStrLn $ show $ pocetCifier (read n) (read b)

pocetCifier :: Int -> Int -> Int
pocetCifier cislo baza
	| cislo < baza = 1
	| otherwise = (pocetCifier (div cislo baza) baza) + 1
