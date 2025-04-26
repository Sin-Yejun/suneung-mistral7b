import json
import os
input_path = "C:/Users/yejun/Desktop/Projects/suneung-mistral7b/backup_data/json/"

output_path = "C:/Users/yejun/Desktop/Projects/suneung-mistral7b/data/processed/json/"
file_list = ['korean2024_3월', 'korean2024_6월',
            'korean2024_9월', 'korean2023_3월',
            'korean2023_6월', 'korean2023_9월',
            'korean2022_3월', 'korean2022_6월',
            'korean2022_9월']
file_list.sort()

answer_path = "C:/Users/yejun/Desktop/Projects/suneung-mistral7b/data/processed/txt/해설/"

answer_files = os.listdir(answer_path)


for i in range(len(file_list)):
    file = file_list[i]
    answer = answer_files[i]
    answers = []
    with open(f"{answer_path+answer}", "r", encoding="utf-8") as f:
            lines = f.readlines()
    for line in lines:
         answers.append(line.strip())
    print(len(answers))
    with open(f"{input_path+file}.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    index = 0
    for section in data:
        for problem in section["problems"]:
            problem["solution"] = answers[index]
            index += 1
    
    with open(f"{output_path+file}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{file} 변환 완료")
