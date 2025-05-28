#This tool converts ARPAbet phonetic notation to International Phonetic Alphabet (IPA).
#To use this tool simply maintain line 141 to 146 for paths set up and needed function. note that diffsinger doesn't require phoneset document so here you can keep commen out. 
#Source: https://www.leskoff.com/arpabet-to-ipa
#Adjusted base on PHOIBLE, e.g. some symbols and discard stress, long/short

ARPAbet_to_IPA_dict = {
  "<SP>":"SP",
  "<AP>":"AP",
  "HH":"h",
  "W":"w",
  "EH1":"ɛ",
  "R":"ɹ", #changed from "r"
  "DH":"ð",
  "AH0":"ə",
  "N":"n",
  "AO1":"ɔ",
  "TH":"θ",
  "IH1":"ɪ",
  "D":"d",
  "M":"m",
  "IY1":"i",
  "T":"t",
  "S":"s",
  "AH1":"ə",
  "Z":"z",
  "V":"v",
  "ER0":"ɚ", #changed from "ər",
  "F":"f",
  "UH1":"ʊ",
  "L":"l",
  "IY0":"i",
  "P":"p",
  "AY1":"aɪ",
  "AA1":"ɑ",
  "IH0":"ɪ",
  "NG":"ŋ",
  "EY1":"eɪ",
  "AE1":"æ",
  "AW1":"aʊ",
  "UW1":"u",
  "Y":"j",
  "B":"b",
  "SH":"ʃ",
  "OW1":"oʊ",
  "JH":"d̠ʒ", #changed from "dʒ",
  "K":"k",
  "ER1":"ɚ", #changed from "ər",
  "UW0":"u",
  "G":"ɡ",
  "AO0":"ɔ",
  "EH0":"ɛ",
  "AH2":"ə",
  "IH2":"ɪ",
  "OW2":"oʊ",
  "CH":"t̠ʃ", #changed from "tʃ",
  "AY2":"aɪ",
  "ZH":"ʒ",
  "OW0":"oʊ",
  "OY1":"ɔɪ",
  "AA2":"ɑ",
  "EH2":"ɛ",
  "EY2":"eɪ",
  "AE0":"æ",
  "AY0":"aɪ",
  "IY2":"i",
  "UW2":"u",
  "AW2":"aʊ",
  "AE2":"æ",
  "UH0":"ʊ",
  "UH2":"ʊ",
  "ER2":"ɚ", #changed from "ər",
  "EY0":"eɪ",
  "AO2":"ɔ",

}


import json 
import os 

def convert_ARPAbet_to_IPA_metadata(file,output_dir):
    # Read the input file
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Process each entry in the metadata
    for entry in data:
        if 'ph' in entry:
            # Convert each ARPAbet symbol to IPA
            converted_ph = []
            for symbol in entry['ph']:
                # Remove the language suffix (e.g., "_en")
                base_symbol = symbol.split('_')[0]
                # Convert using the dictionary
                if base_symbol in ARPAbet_to_IPA_dict:
                    converted_ph.append(ARPAbet_to_IPA_dict[base_symbol])
                else:
                    # If not found in dictionary, keep original
                    converted_ph.append(symbol)
                    print(f"{symbol} is not found so it is not converted")
            entry['ph'] = converted_ph
    
    # Create output filename
    output_file = os.path.join(output_dir, os.path.basename(file))
    
    # Write the converted data to new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Conversion metadata complete. Output saved to {output_file}")

def convert_ARPAbet_to_IPA_phone_set(file,output_dir):
    # Read the input file
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert each ARPAbet symbol to IPA
    converted_data = []
    for symbol in data:
      # Remove the language suffix (e.g., "_en")
      base_symbol = symbol.split('_')[0]
      # Convert using the dictionary
      if base_symbol in ARPAbet_to_IPA_dict:
        converted_data.append(ARPAbet_to_IPA_dict[base_symbol])
      else:
        # If not found in dictionary, keep original
        converted_data.append(symbol)
        print(f"{symbol} is not found so it is not converted")
    
    # Create output filename
    output_file = os.path.join(output_dir, os.path.basename(file))
    
    # Write the converted data to new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, indent=2, ensure_ascii=False)
    
    print(f"Conversion phone_set complete. Output saved to {output_file}")


# Call the function with your file path
output_dir = "/path/to/your/folder"
metadata_ARPAbet = "/path/to/your/folde/metadata.json"
#phone_set_ARPAbet = "/path/to/your/folde/phone_set.json"

convert_ARPAbet_to_IPA_metadata(metadata_ARPAbet,output_dir)
#convert_ARPAbet_to_IPA_phone_set(phone_set_ARPAbet,output_dir)