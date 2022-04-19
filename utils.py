def approx_coordinates(lat_, long_, decimal=5):
	"""	 
	rounds latitude and longitude coordinates to a given decimal place 
	default is 5.
	"""
	return (round(lat_, decimal), round(long_, decimal))