import argparse
import os
from googletrans import Translator
from googletrans import constants

RETRY_TIMES = 10
#translator = Translator()
translator = Translator(constants.DEFAULT_SERVICE_URLS)
#translator = Translator(service_urls=[
#      'translate.google.com',
#      'translate.google.co.kr',
#    ])

def is_valid_srt_file(file_path):
    """
    Checks if the given file is a valid .srt subtitle file.
    """
    try:
        with open(file_path, "r", encoding='utf-8-sig') as f:
            # Read the first line and check if it starts with a number (subtitle index)
            first_line = f.readline().strip()
            if first_line.isdigit():
                return True
            else:
                return False
    except FileNotFoundError:
        return False
    
def translate_subtitles(input_file, src_lang='en', dest_lang='zh-hk'):

    # Open the file in read mode ('r')
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_filename}.{src_lang}_{dest_lang}.srt"
    with open(input_file, 'r', encoding='utf-8-sig') as src, open(output_file, 'w', encoding='utf-8') as dst:
        while True:
            line = src.readline()
            if not line:
                break
            line = line.strip()
            if line == '':
                dst.write('\n')
            else:
                if line.isdigit(): # Check if the line is a subtitle index
                    dst.write(f"{line}\n")
                else:
                    for i in range(RETRY_TIMES):
                        try:
                            translation  = translator.translate(line, src=src_lang, dest=dest_lang)
                            new_line = line+"/"+translation.text
                            dst.write(new_line+'\n')
                            print(new_line)
                            break
                        except Exception as e:
                            if i == RETRY_TIMES-1:
                                # Log the exception and write the original line to the destination file
                                print(f"An exception occurred: {e}")
                                print(f"Exception traceback: {e.__traceback__}")
                                dst.write(line+'\n')
                            else:
                                continue
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate subtitles from one language to another.")
    parser.add_argument("input_file", help="Input subtitle file (.srt)")
    parser.add_argument("src_lang", help="Source language (e.g., 'en' for English)")
    parser.add_argument("dest_lang", help="Destination language (e.g., 'zh-hk' for Traditional Chinese)")
    args = parser.parse_args()
    if is_valid_srt_file(args.input_file):
        translate_subtitles(args.input_file, args.src_lang, args.dest_lang)
    else:
        print(f"{args.input_file} is not a valid .srt file.")