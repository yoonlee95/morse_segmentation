# -*- coding: utf-8 -*-


def find_translation(language):
    language = language.lower()
    iso639_dict = {}
    with open("iso639.txt") as f:
        contents = f.readlines()
        for content in contents:
            c = content.split("|")
            for name in c[3].split(";"):
                iso639_dict[name.strip().lower()] = c[0]
    return iso639_dict[language]





if __name__ == "__main__":
    print find_translation("KOREAN")

# you may also want to remove whitespace characters like `\n` at the end of each line
#content = [x.strip() for x in content]