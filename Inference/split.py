# -*- coding: utf-8 -*- # with open("cleaned_2000_sejong_gold.txt") as f: #     content = f.readlines()
# # you may also want to remove whitespace characters like `\n` at the end of each line
# # content = [x.split()[0] for x in content] 
# content = [x.split(" ", 1)[1] for x in content] 
# f = open('cleaned_2000_sejong_output_gold.txt', 'w')

# for i in content:
#     f.write(i)

# with open("600k_75_output.txt") as f:
#     content = f.readlines()
# # you may also want to remove whitespace characters like `\n` at the end of each line
# # content = [x.split()[0] for x in content] 
# content = [x.strip() for x in content] 

# f = open('cleaned_600k_75_output.txt', 'w')
# for i in content:
#     f.write(i + "\n")

with open("600k_75_output.txt") as f:
    content1 = f.readlines()
with open("cleaned_2000_sejong_output_gold.txt") as f:
    content2 = f.readlines()
j = 0

f = open('sejong_different.txt', 'w')

content1 = [x.strip() for x in content1] 
content2 = [x.strip() for x in content2] 
for i in range (len(content2)):
    if content1[i] != content2[i]:
        j += 1
        f.write(content1[i] +" " + content2[i] + "\n")
print j
# you may also want to remove whitespace characters like `\n` at the end of each line
# content = [x.split()[0] for x in content] 
# content = [x.strip() for x in content] 

# f = open('cleaned_2000_sejong_output_cleaned.txt', 'w')
# for i in content:
#     f.write(i + "\n")
