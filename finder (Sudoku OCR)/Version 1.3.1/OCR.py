import tesseract
api = tesseract.TessBaseAPI()

def ocr_singledigit(image):
	api.Init(".","eng",tesseract.OEM_DEFAULT)
	api.SetVariable("tessedit_char_whitelist", "123456789")
	api.SetPageSegMode(6)
	tesseract.SetCvImage(image,api)
	char = api.GetUTF8Text()
	char = char.replace(" ","").strip()
	
	if len(char) == 0:
		return "x"
	return int(char)
	
def split_len(item, length):
    return [item[i:i+length] for i in range(0, len(item), length)]

def getcorners(c,points):
    x = c[0]
    y = c[1]
    top_left_corner_index = 10 * y + x
    down_right_corner_index = top_left_corner_index + 11
    
    top_left_corner = points[top_left_corner_index]
    down_right_corner = points[down_right_corner_index]

    return (top_left_corner[0],down_right_corner[0],top_left_corner[1],down_right_corner[1])