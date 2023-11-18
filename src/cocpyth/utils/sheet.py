import shutil
import urllib.request

COC_GREYSCALE_1920_SHEET_URL = "https://www.chaosium.com/content/FreePDFs/CoC/Character%20Sheets/V2/CoC7%20PC%20Sheet%20-%20Auto-Fill%20-%201920s%20-%20Standard%20-%20Greyscale.pdf"
COC_COLOR_1920_SHEET_URL = "https://www.chaosium.com/content/FreePDFs/CoC/Character%20Sheets/V2/CoC7%20PC%20Sheet%20-%20Auto-Fill%20-%201920s%20-%20Standard%20-%20Color.pdf"



def download_charactersheet(file_name, color=False):

    url = COC_GREYSCALE_1920_SHEET_URL
    if color:
        url = COC_COLOR_1920_SHEET_URL
    
    with urllib.request.urlopen(url) as response,\
        open(file_name, 'wb') as outf:
        shutil.copyfileobj(response, outf)
    
    return file_name


if __name__ == "__main__":
    download_charactersheet("sheet.pdf")