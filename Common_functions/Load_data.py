# codes for loading datasets
import os.path
import random
import sys


def load_Births(start=1, end=12, scale=1):
    """
    load the Births dataset
    scale indicates the sizes of datasets are divided by scale (default scale = 1)
    start and end imply the start and end month
    """

    # root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.dirname(base_dir)
    sys.path.append(base_dir)

    # read birth file
    file = base_dir + "/Datasets/US_births_2000-2014_SSA.csv"
    data_line = []
    with open(file, "r") as f:
        data = f.readlines()
        for line in data:
            line1 = line.strip('\n')
            data_line.append(line1)

    # delete the attribute line
    # example of data line: 2000,1,1,6,9083 - year:2000, month:1, day:1, weekday:6, frequency: 9083
    del data_line[0]

    # load plaintexts
    yearly_plaintext = {}

    for i in data_line:
        item = i.split(",")
        # item_pair [101,9083]: 101-1st January, 9083-frequency
        item_pair = [int(item[1]) * 100 + int(item[2]), int(item[4]) // scale]
        if start <= int(item[1]) < (end + 1):
            if int(item[0]) in yearly_plaintext:
                yearly_plaintext[int(item[0])].append(item_pair)
            else:
                yearly_plaintext[int(item[0])] = [item_pair]

    return yearly_plaintext


def load_Apls():
    """load the Apls dataset"""

    # root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.dirname(base_dir)
    sys.path.append(base_dir)

    # read Apls file
    file = base_dir + "/Datasets/insurance.csv"
    data_line = []
    with open(file, "r") as f:
        data = f.readlines()
        for line in data:
            line1 = line.strip('\n')
            data_line.append(line1)

    # delete the attribute line
    # example of data line: 2016,2016 Q1,0 to 17,Male,175678
    # year:2016, quarter:Q1, age group:0 to 17, gender:Male frequency: 175678
    del data_line[0]

    # load plaintexts according to age groups and gender
    age = [[0 for i in range(7)] for j in range(10)]
    gender = [[0, 0] for i in range(35)]

    for i in range(len(data_line)):
        item = data_line[i].split(",")

        # age groups
        if item[2] == '0 to 17':
            if item[3] == 'Male':
                age[2 * (2020 - int(item[0]))][0] += int(item[4])
                gender[7 * (2020 - int(item[0]))][0] += int(item[4])
            else:
                age[2 * (2020 - int(item[0])) + 1][0] += int(item[4])
                gender[7 * (2020 - int(item[0]))][1] += int(item[4])
        elif item[2] == '18 to 25':
            if item[3] == 'Male':
                age[2 * (2020 - int(item[0]))][1] += int(item[4])
                gender[7 * (2020 - int(item[0]))+1][0] += int(item[4])
            else:
                age[2 * (2020 - int(item[0])) + 1][1] += int(item[4])
                gender[7 * (2020 - int(item[0])) + 1][1] += int(item[4])
        elif item[2] == '26 to 34':
            if item[3] == 'Male':
                age[2 * (2020 - int(item[0]))][2] += int(item[4])
                gender[7 * (2020 - int(item[0]))+2][0] += int(item[4])
            else:
                age[2 * (2020 - int(item[0])) + 1][2] += int(item[4])
                gender[7 * (2020 - int(item[0]))+2][1] += int(item[4])
        elif item[2] == '35 to 44':
            if item[3] == 'Male':
                age[2 * (2020 - int(item[0]))][3] += int(item[4])
                gender[7 * (2020 - int(item[0]))+3][0] += int(item[4])
            else:
                age[2 * (2020 - int(item[0])) + 1][3] += int(item[4])
                gender[7 * (2020 - int(item[0])) + 3][1] += int(item[4])
        elif item[2] == '45 to 54':
            if item[3] == 'Male':
                age[2 * (2020 - int(item[0]))][4] += int(item[4])
                gender[7 * (2020 - int(item[0]))+4][0] += int(item[4])
            else:
                age[2 * (2020 - int(item[0])) + 1][4] += int(item[4])
                gender[7 * (2020 - int(item[0])) + 4][1] += int(item[4])
        elif item[2] == '55 to 64':
            if item[3] == 'Male':
                age[2 * (2020 - int(item[0]))][5] += int(item[4])
                gender[7 * (2020 - int(item[0]))+5][0] += int(item[4])
            else:
                age[2 * (2020 - int(item[0])) + 1][5] += int(item[4])
                gender[7 * (2020 - int(item[0])) + 5][1] += int(item[4])
        elif item[2] == '65+':
            if item[3] == 'Male':
                age[2 * (2020 - int(item[0]))][6] += int(item[4])
                gender[7 * (2020 - int(item[0]))+6][0] += int(item[4])
            else:
                age[2 * (2020 - int(item[0])) + 1][6] += int(item[4])
                gender[7 * (2020 - int(item[0])) + 6][1] += int(item[4])

    return age, gender


def Merge_Dictionary(dict1, dict2):
    return dict2.update(dict1)


def load_PBN():
    """load the PBN dataset"""

    # root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.dirname(base_dir)
    sys.path.append(base_dir)

    # read names file
    path = base_dir + "/Datasets/names"
    files = ["1970", "1980", "1990", "2000", "2010"]
    total_list = []

    for file in files:
        data_list = []
        first_line = 0
        with open(path + "/" + file + ".csv", "r", encoding='UTF-8') as f:
            data = f.readlines()
            for line in data:
                if first_line == 0:
                    first_line = 1
                    continue
                line1 = line.strip('\n')
                data_list.append(line1)
            total_list.append(data_list)

    # build a dictionary for names and their counts
    PBN_dir = [{} for i in range(len(total_list))]
    for i in range(len(total_list)):
        for j in range(len(total_list[i])):
            line = total_list[i][j].split(",")
            PBN_dir[len(total_list) - i - 1][line[0]] = int(line[1])
            PBN_dir[len(total_list) - i - 1][line[2]] = int(line[3])

    # build a dataset consisting of names which appear in the first decade
    # and most decades
    map_count = {}
    total_count = len(total_list)
    for i in PBN_dir[0]:
        count = 0
        for j in range(total_count):
            if i in PBN_dir[j]:
                count += 1
        if count > 4:
            map_count[i] = count

    # print(len(map_count))
    # mapping names to integers for encryption
    map_integer = {}
    for i in PBN_dir:
        Merge_Dictionary(i, map_integer)

    map_name_list = sorted(map_integer.items(), key=lambda d: d[0])

    map_int = 0
    for i in map_name_list:
        map_integer[i[0]] = map_int
        map_int += 1

    PBN_insertion_dataset = [[] for i in range(total_count)]

    for i in range(total_count):
        for j in PBN_dir[i]:
            if j in map_count:
                PBN_insertion_dataset[i] += [map_integer[j] for k
                                             in range(PBN_dir[i][j])]

        random.shuffle(PBN_insertion_dataset[i])

    return PBN_insertion_dataset
