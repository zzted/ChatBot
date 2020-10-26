class File_reader:
    def __init__(self):
        self.training_data = []
        self.training_label = []

    def read(self, file_dir):
        with open(file_dir) as fp:
            cluster = [x.strip('\n') for x in fp.readlines()]

        label = '0'

        for sample in cluster:
            if 'Cluster' in sample:
                label = sample.split('_')[0]
                continue
            if label == '0':
                continue
            self.training_data.append(sample.split('@')[0])
            self.training_label.append(int(label))





