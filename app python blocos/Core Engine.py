def extract_unit_and_description(raw_text):
    words = raw_text.split()
    
    if not words:
        return raw_text, "-"
        
    last_word = words[-1]
    second_last = words[-2] if len(words) > 1 else ""
    
    if second_last == "MES" and last_word == "R":
        return " ".join(words[:-2]), "MES R"
        
    if len(last_word) <= 6:
        return " ".join(words[:-1]), last_word
        
    return raw_text, "-"

def parse_line_logic(line_text, current_context_family, sequence_flag):
    regex_price_anchor = re.compile(r"(R\$\s?[\d\.]+,[\d]{2})$")
    regex_code_anchor = re.compile(r"^([A-Z0-9\.]{7,})")
    
    match_code = regex_code_anchor.search(line_text)
    
    if not match_code:
        return "SKIP", None, current_context_family, sequence_flag
        
    code_value = match_code.group(1)
    match_price = regex_price_anchor.search(line_text)
    
    if match_price:
        price_value = match_price.group(1)
        middle_text = line_text[len(code_value):].replace(price_value, "").strip()
        
        description, unit = extract_unit_and_description(middle_text)
        
        product_data = {
            "Family Hierarchy": current_context_family,
            "Code": code_value,
            "Description": description,
            "Unit": unit,
            "Price": price_value
        }
        return "PRODUCT", product_data, current_context_family, False
        
    else:
        potential_family_name = line_text[len(code_value):].strip()
        
        if len(potential_family_name) > 3:
            if sequence_flag:
                updated_family = f"{current_context_family} | {potential_family_name}"
            else:
                updated_family = potential_family_name
                
            return "HIERARCHY", updated_family, updated_family, True
            
    return "SKIP", None, current_context_family, sequence_flag
