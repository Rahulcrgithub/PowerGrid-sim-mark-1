import csv
import os

class CSVLogger:
    def __init__(self, folder="logs", base_filename="power_data", max_file_size=50 * 1024 * 1024):  # 50 MB
        self.folder = folder
        self.base_filename = base_filename
        self.max_file_size = max_file_size
        self.file_index = 1
        os.makedirs(self.folder, exist_ok=True)
        self.current_file = self._get_new_file()
        self.writer = None
        self._open_writer()

    def _get_new_file(self):
        return os.path.join(self.folder, f"{self.base_filename}_{self.file_index}.csv")

    def _open_writer(self):
        if os.path.exists(self._get_new_file()):
            file_size = os.path.getsize(self._get_new_file())
            if file_size > self.max_file_size:
                self.file_index += 1
        self.current_file = self._get_new_file()
        is_new = not os.path.exists(self.current_file)
        self.csv_file = open(self.current_file, "a", newline='')
        self.writer = csv.writer(self.csv_file)
        if is_new:
            self.writer.writerow(["Time (s)", "Voltage (V)", "Current (A)", "Active Power (kW)", 
                                  "Reactive Power (kVAR)", "Apparent Power (kVA)", 
                                  "Power Factor", "Frequency (Hz)", "Load (kW)",
                                  "Fault Status", "Harmonics Status"])

    def log(self, row):
        if os.path.getsize(self.current_file) > self.max_file_size:
            self.csv_file.close()
            self.file_index += 1
            self._open_writer()
        self.writer.writerow(row)
        self.csv_file.flush()

    def close(self):
        self.csv_file.close()
