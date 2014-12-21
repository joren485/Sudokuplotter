""""""
import tesseract
API = tesseract.TessBaseAPI()

def ocr_singledigit(image):
    """Recognize a singe digit on a small image"""
    API.Init(".", "eng", tesseract.OEM_DEFAULT)
    API.SetVariable("tessedit_char_whitelist", "123456789")
    API.SetPageSegMode(6)
    tesseract.SetCvImage(image, API)
    CHAR = API.GetUTF8Text()
    CHAR = CHAR.replace(" ", "").strip()
    
    if len(CHAR) == 0:
        return "x"
    return int(CHAR)
    
def split_len(item, length):
    """Split a item into a list, split on length"""
    return [item[i:i+length] for i in range(0, len(item), length)]

def getcorners(C, points):
    """Calculate the corner points from point coordinates"""
    x = C[0]
    y = C[1]
    top_left_corner_index = 10 * y + x
    down_right_corner_index = top_left_corner_index + 11
    
    top_left_corner = points[top_left_corner_index]
    down_right_corner = points[down_right_corner_index]

    return (top_left_corner[0], down_right_corner[0], top_left_corner[1], down_right_corner[1])
