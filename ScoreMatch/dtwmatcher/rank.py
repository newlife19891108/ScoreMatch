def rank(reference,candidates,chroma_function,dtw_function):
	template=chroma_function(reference)
	score_list =[]
	for candidate in candidates:
		score_list.append((candidate,dtw_function(template,chroma_function(candidate))))
	return sorted(score_list, key=lambda candidate: candidate[1]) 

def rank_analyzables(reference,candidates,dtw_function):
	sorted_list = []
	template = reference.get_chromagram()
	for candidate in candidates:
		sorted_list.append((candidate,dtw_function(template,candidate.get_chromagram())))
	sorted_list.sort(key = lambda candidate: candidate[1])
	return sorted_list