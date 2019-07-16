import json

class File_loader:
	def __init___(self):
		pass

	def write_json(self, file_path, attriboots_dic):
		with open(file_path, 'wt', encoding='utf-8') as output_file:
		    json.dump(attriboots_dic, output_file, ensure_ascii=False, indent=2)
		    return True

	def read_json(self, file_path):
		with open(file_path) as input_file:
			return json.load(input_file)