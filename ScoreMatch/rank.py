def rank(reference,candidates,chromaFunction,dtwFunction):
	template=chromaFunction(reference)
	scoreList =[]
	for candidate in candidates:
		scoreList.append((candidate,dtwFunction(template,chromaFunction(candidate))))
	return sorted(scoreList, key=lambda candidate: candidate[1]) 

