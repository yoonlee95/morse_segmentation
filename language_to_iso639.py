# -*- coding: utf-8 -*-


def find_translation(language):
    try:
        language = language.lower()
        iso639_dict = {}
        with open("iso639.txt") as f:
            contents = f.readlines()
            for content in contents:
                c = content.split("|")
                for name in c[3].split(";"):
                    if len(c[2]) > 1:
                        iso639_dict[name.strip().lower()] = c[2]
                    else:
                        iso639_dict[name.strip().lower()] = c[0]
        return iso639_dict[language]
    except:
        print "Could Not find Language"
        exit()




if __name__ == "__main__":
        print find_translation("KOREddAN")

# you may also want to remove whitespace characters like `\n` at the end of each line
#content = [x.strip() for x in content]