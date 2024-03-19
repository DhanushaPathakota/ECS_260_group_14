import csv
import matplotlib.pyplot as plt
import numpy as np

def remove_outliers(data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    cleaned_data = [x for x in data if x >= lower_bound and x <= upper_bound]
    return cleaned_data

def draw_box_plot(data, x):
    plt.figure(figsize=(4, 6))
    plt.boxplot(data)
    plt.title('Box Plot')
    plt.xlabel(x)
    plt.ylabel('Values')
    plt.grid(True)
    plt.show()

csv.field_size_limit(1024 * 1024 * 1024)

def fetch_message_info(csv_file, data_names):
    related_data = []
    with open(csv_file, mode='r', encoding='latin-1') as file:
        reader = csv.reader(file)
        first_row = next(reader)
        print(first_row)
        index_list = []
        for data_name in data_names:
            index_list.append(first_row.index(data_name))

        i = 0
        data_list = list()
        j = 100000
        for line in reader:
            i += 1
            if i % 10000 == 0:
                print(j, i)
            if i == 100000:
                with open('message_data_' + str(j) + '.csv', 'w', newline='') as csvfile:
                    spamwriter = csv.writer(csvfile)
                    spamwriter.writerow(data_names)
                    for row in data_list:
                        spamwriter.writerow(row)
                i = 0
                data_list = list()
                j += 1
            data_item = list()
            for index in index_list:
                data_item.append(line[index])
            # print(data_item)
            data_list.append(data_item)

class ProjectMessageManager:
    def __init__(self):
        self.count = 0
        self.senders = dict()
        self.number_sender = 0
        self.number_active_sender = 0
        self.length = 0
        self.average_length = 0
        self.period = 0
        self.frequency = 0
        self.

    def __str__(self):
        return str(self.count) + ", " + str(self.average_length) + ", " \
               + str(self.senders) + ", " + str(self.number_active_sender)


def analyze_data():
    message_data = dict()
    for j in range(100000, 100014):
        print(j)
        csv_file = "message_data_" + str(j) + ".csv"
        with open(csv_file, mode='r', encoding='latin-1') as file:
            reader = csv.reader(file)
            next(reader)
            for line in reader:
                prj_id = int(line[0])
                if prj_id not in message_data.keys():
                    message_data[prj_id] = ProjectMessageManager()
                message_data[prj_id].count += 1
                message_data[prj_id].length += len(line[5])
                # print(line[5])
                if line[2] not in message_data[prj_id].senders.keys():
                    message_data[prj_id].senders[line[2]] = 0
                message_data[prj_id].senders[line[2]] += 1

    for prj_id in sorted(list(message_data.keys())):
        message_data[prj_id].average_length = message_data[prj_id].length / message_data[prj_id].count
        for v in message_data[prj_id].senders.values():
            message_data[prj_id].number_sender += 1
            if v > 50:
                message_data[prj_id].number_active_sender += 1
        print(prj_id, message_data[prj_id])

    with open("updated_metrics_main.csv", mode='r', encoding='latin-1') as file:
        reader = csv.reader(file)
        first_row = next(reader)
        print(first_row)
        index = first_row.index("Incubation_Period(days)")

        for line in reader:
            prj_id = int(line[0])
            if line[index] != "":
                if prj_id in message_data.keys():
                    message_data[prj_id].period = float(line[index])
                    message_data[prj_id].frequency = float(message_data[prj_id].count) / message_data[prj_id].period

    with open('prj_communication.csv', 'w', newline='') as file:
        spamwriter = csv.writer(file)
        data_names = ["prj_id", "count", "average_length", "number_active_senders", "frequency"]
        spamwriter.writerow(data_names)

        for prj_id in sorted(list(message_data.keys())):
            row = list()
            row.append(prj_id)
            row.append(message_data[prj_id].count)
            row.append(message_data[prj_id].average_length)
            row.append(message_data[prj_id].number_active_sender)
            row.append(message_data[prj_id].frequency)
            spamwriter.writerow(row)


def box_plots(csv_file, data_names):
    with open(csv_file, mode='r', encoding='latin-1') as file:
        reader = csv.reader(file)
        first_row = next(reader)
        print(first_row)
        index_list = []
        for data_name in data_names:
            index_list.append(first_row.index(data_name))

        data_list = list()
        for i in range(len(data_names)):
            data_list.append(list())
        for line in reader:
            if line[index_list[3]] != "0":
                for i in range(len(index_list)):
                    data_list[i].append(float(line[index_list[i]]))
        for i in range(len(data_list)):
            data_ls = remove_outliers(data_list[i])
            draw_box_plot(data_ls, data_names[i])



                # test
# csv_file = 'lists_2019_8.csv'
csv_file = 'messages_2019_8.csv'

data_names = ['list', 'senderalias', 'senderaliasid', 'datetime', 'subject', 'body', 'from_commit']

# fetch_message_info(csv_file, data_names)
# analyze_data()

csv_file = 'prj_communication.csv'
data_names = ['count', 'average_length', 'number_active_senders', 'frequency']

box_plots(csv_file, data_names)
