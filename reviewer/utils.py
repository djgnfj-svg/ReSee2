
from re import L


def dateCalculation(_baseDate, _StudyList):
	return_list = []
	for s_list in _StudyList:
		temp = _baseDate-s_list.created_at
		temp_day = temp.days
		print("지나간 날짜 : ", temp_day)
		print("reviwe_count : ",s_list.review_count)
		if temp_day == 0 and s_list.review_count < 1:
			return_list.append(s_list)
		elif temp_day > 1 and temp_day < 3 and s_list.review_count < 2:
			return_list.append(s_list)
		elif temp_day > 3 and temp_day < 7 and s_list.review_count < 3:
			return_list.append(s_list)
		elif temp_day > 7 and temp_day < 14 and s_list.review_count < 4:
			return_list.append(s_list)
		elif temp_day > 14 and temp_day < 31 and s_list.review_count < 5:
			return_list.append(s_list)
		elif temp_day > 31 and temp_day < 93 and s_list.review_count < 6:
			return_list.append(s_list)
		elif temp_day > 93 and temp_day < 182 and s_list.review_count < 7:
			return_list.append(s_list)
		elif temp_day > 182 and s_list.review_count < 8:
			return_list.append(s_list)
	
	return(return_list)

