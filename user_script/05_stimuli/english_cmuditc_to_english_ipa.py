#this tool is used to convert english cmuditc to english ipa
import json 
CMU_to_IPA_dict = {
    'b': 'b',
    'ch': 't̠ʃ',
    'd': 'd',
    'dh': 'ð',
    'f': 'f',
    'g': 'ɡ',
    'hh': 'h',
    'jh': 'd̠ʒ',
    'k': 'k',
    'l': 'l',
    'm': 'm',
    'n': 'n',
    'ng': 'ŋ',
    'p': 'p',
    'r': 'ɹ',
    's': 's',
    'sh': 'ʃ',
    't': 't',
    'th': 'θ',
    'v': 'v',
    'w': 'w',
    'y': 'j',
    'z': 'z',
    'zh': 'ʒ',

    # vowel
    'aa': 'ɑ',
    'ae': 'æ',
    'ah': 'ə',
    'ao': 'ɔ',
    'aw': 'aʊ',
    'ay': 'aɪ',
    'ai': 'aɪ',  
    'eh': 'ɛ',
    'ei': 'eɪ',
    'er': 'ɚ',
    'ey': 'eɪ',
    'ih': 'ɪ',
    'iy': 'i',
    'ow': 'oʊ',
    'ou': 'oʊ',
    'oy': 'ɔɪ',
    'uh': 'ʊ',
    'uw': 'u',

    # special symbol
    'AP': 'AP',  
    'SP': 'SP',  
    '<ap>': 'AP',
    '<sp>': 'SP'
}

def convert_cmu_to_ipa(ph_seq):
    phonemes = ph_seq.split()
    ipa_phonemes = []
    missing_phonemes = set()
    
    for phoneme in phonemes:
        if phoneme in ['AP', 'SP']:
            ipa_phonemes.append(phoneme)
            continue
            
        try:
            base_phoneme = ''.join([c for c in phoneme if not c.isdigit()]).lower()
            
            if base_phoneme in CMU_to_IPA_dict:
                ipa_phonemes.append(CMU_to_IPA_dict[base_phoneme])
            else:
                missing_phonemes.add(phoneme)
                ipa_phonemes.append(phoneme)  
        except Exception as e:
            print(f"Error processing phoneme '{phoneme}': {str(e)}")
            ipa_phonemes.append(phoneme)
    
    if missing_phonemes:
        print(f"Warning: These phonemes were not found in the dictionary: {', '.join(missing_phonemes)}")
    
    return ' '.join(ipa_phonemes)

def process_ds_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        if 'ph_seq' in item:
            item['ph_seq'] = convert_cmu_to_ipa(item['ph_seq'])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

input_file = '/path/to/your/cmudict-xxx.ds'  # Replace with your input file
output_file = '/path/to/your/ipa-xxx.ds'  # Replace with desired output file
process_ds_file(input_file, output_file)