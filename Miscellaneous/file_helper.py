# Installation:
# Create a file next to this script named: {file}.txt(See file value in configuration above)
# Create folders in and out

# Configuration
file = 'identifier_db.txt'
folder_in = 'dest_download'
folder_out = 'dest_to_check'
delimiter = ';'


import os
in_path = os.path.join(os.getcwd(), folder_in)
out_path = os.path.join(os.getcwd(), folder_out)
replacer = ','

#############
## Helpers ##
#############

# START formatter( str )
def formatter( str ):
    global delimiter
    global replacer
    return str.strip().replace(delimiter, replacer)
# END formatter( str )


##########
## Read ##
##########

# START get_dico()
def get_dico():
    global file
    global delimiter

    # Get file
    dico = {}
    f_read = open(file, 'r');
    lines = f_read.readlines()

    # Put data in a dictionnary(key -> value)
    for line in lines:
        line_strip = line.strip()
        # print('Line: ' + lineStrip)
        words = line_strip.split(delimiter)

        identifier = None
        title = None
        i = 0
        for word in words:
            if i == 0:
                # print('    Identifier: ' + word)
                identifier = word
            elif i == 1:
                # print('    Title: ' + word)
                title = word
            else:
                break;
            i += 1

        # Fill in the dictionnary and handle errors
        if identifier is not None and identifier in dico:
            print('ERROR: Identifier found multiple times -> %s (getDico)' % (identifier))
        elif identifier is not None and title is not None:
            dico[identifier] = title
        else:
            print('ERROR: Incomplete line -> %s;%s (getDico)' % (identifier, title))

    f_read.close()
    return dico
# END get_dico()


############
## Exists ##
############

# Check if an identifier exists in the configured file
# START exists(identifier)
def exists(identifier):
    formatted_identifier = formatter(identifier)
    return formatted_identifier in get_dico()
# END exists(identifier)


###########
## Write ##
###########

# Write an identifier and its associated values into the configured file
# START write( identifier, title, creator, licenseurl )
def write( identifier, title, creator, licenseurl ):
    global file
    formatted_identifier = formatter(identifier)
    formatted_title = formatter(title)
    formatted_creator = formatter(creator)
    formatted_licenseurl = formatter(licenseurl)

    # Check identifier is not already in the file
    if exists(formatted_identifier):
        print('ERROR: Identifier exists -> %s (write)' % (formatted_identifier))
        return
        
    f_write = open(file, 'a'); # Appending mode to add data to the end of the file
    f_write.write(formatted_identifier + delimiter + formatted_title + delimiter + formatted_creator + delimiter + formatted_licenseurl + '\n')
    f_write.close()
# END write( identifier, title, creator, licenseurl )


#####################
## Rename and move ##
#####################

# Rename and move the files
# Uses the configured in and out repositories
# Reads the configured file identifier(key) -> tile(value)
# START rename_and_move()
def rename_and_move():
    global os
    global in_path
    global out_path

    # Get all the identifiers with their file name
    dico = get_dico()
    for identifier in dico:
        item_path = os.path.join(in_path, identifier)

        # Check the repository exists
        if not os.path.exists(item_path):
            continue

        # Get all the files inside the directory
        files = [f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))]

        # Check there is only one file to rename
        count = 0
        for file in files:
            count += 1

        if not count == 1:
            print('ERROR: ' + str(count) + '(1 expected) files found in the folder ' + identifier + ' (updateTitles)')
            continue

        # Update file name
        for file in files:
            (oldName, ext) = os.path.splitext(file)
            src = os.path.join(item_path, file)
            dst = os.path.join(out_path, dico[identifier] + ext)

            if not os.path.exists(dst):
                os.rename(src, dst) # It renames and moves the file
                print('Renamed ' + src + ' -> ' + dst)
                # Delete the not used anymore folder
                os.rmdir(item_path)
            else:
                print('ERROR: The file ' + file + ' can\'t be renamed and moved, it already exists in the out folder (updateTitles)')
                continue
# END rename_and_move()


    
