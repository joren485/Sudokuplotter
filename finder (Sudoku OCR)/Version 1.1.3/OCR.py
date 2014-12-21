import tesseract
api = tesseract.TessBaseAPI()

def ocr_singledigit(image):
	api.Init(".","eng",tesseract.OEM_DEFAULT)
	api.SetVariable("tessedit_char_whitelist", "123456789")
	api.SetPageSegMode(6)
	tesseract.SetCvImage(image,api)
	char=api.GetUTF8Text()
	char=char.replace(" ","").strip()
	
	if len(char) == 0:
		return "_"
	return char
	
def split_len(string, length):
    return [string[i:i+length] for i in range(0, len(string), length)]


