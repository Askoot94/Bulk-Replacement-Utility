def createGlossary(givenText:str):
    # !!!!!!
    # This is wrong, shouldn't be allowed to work for both Files and actual text, seperate them into different functions
    # !!!!!!
    
    # Identify List of terms to replace
    terms = list(dict())

    # Check the last 4 letters in a text, and check if it ends with ".txt" or ".rtf"
    if givenText.find(".txt" or ".rtf", givenText.__len__() - 4) != -1:
        # try to open file
        try:
            # with statement will handle opening and closing the file.
            with open(givenText, "rt", encoding="UTF-8") as glossaryFile:

                # Grab a line from the file
                for singleLine in glossaryFile:
                    tmp = getEntry(singleLine)
                    if tmp != None:
                        terms.append(tmp)

        except Exception as e:
            e.add_note("Requested file was not found.")
    else:
        for line in givenText.splitlines():
            tmp = getEntry(line)
            if tmp != None:
                terms.append(tmp)

    # Sort the Terms in list descending by size key.
    terms.sort(key=getTermSize, reverse=True)

    return terms

def getTermSize(term:dict):
    return term['size']
        
# Gets a Dictionary from a single Line
def getEntry(Line:str):

    # Validate by finding '='
    delim = Line.find("=")

    # If any '=' found then proceed, otherwise ignore.
    if delim != -1:
        # Check for trailing newline
        if Line[Line.__len__()-1] == '\n':
            end = Line.__len__()-1
        else:
            end = Line.__len__()

        # Identify and Store character(s) to remove and insert
        split = dict(find =Line[:delim], replace =Line[delim+1:end], size=delim)
        
        # add the new dictionary to list
        return split
    else:
        return None

# Need to Debug HARD
def replaceTerms(text: str, glossary:list):
    if glossary != [] and text != "":
        send = str()
        
        # seperate text per line
        for line in text.split("\n"):
            # for each dict in glossary
            for term in glossary:
                
                # Check for find and replace terms in given dict
                if "find" and "replace" in term:    
                    line = line.replace(term["find"],term["replace"])
                else:
                    print("Bad Dict recieved")
                    print(term)
            
            # Add new line to end of adjusted line
            send += line + '\n'
                    
        return send
    else:
        return text