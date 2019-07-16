from lxml import etree as ET

from repy.loader import File_loader
from repy.xml import generate_ET_from_JSON, convert_JSON2metaJSON, Document_model

		####################################################
		#  ВЫГРУЗКА ДАННЫХ 								   #
		#						   						   #
		#  Загружаем исходные данные, описание пространст- #
		#  ва имен и описание стрктуры заголовочного тега. #
		####################################################

		# Путь к JSON-файлу с описанием пространства имен
ns_file_path = './data/input/namespace.json'

		# Путь к metaJSON-файлу с описанием структуры заголовка
header_struc_file_path = './data/input/header_struc.json'

		# Путь к JSON-файлу с исходными данными
raw_data_01_file_path = './data/input/raw_data_01.json'

fl = File_loader()

raw_data_dic = fl.read_json(raw_data_01_file_path)
header_dic = fl.read_json(header_struc_file_path)
ns_dic = fl.read_json(ns_file_path)

		####################################################
		#  ПРЕДОБРАБОТКА ДАННЫХ 						   #
		#						   						   #
		#  Для конвертации из JSON в XML необходимо выдел- #
		#  ить теги и создать новый JSON c метатегами.	   #
		####################################################

		# Словарь для добавления метатегов из исходного JSON
temp_data_dic = {
	'#': []
}
		
		####################################################
		# Работа с тегом Series 						   #
		# 												   #
		# Тк много повторений в аттрибутах, проще хранить  # 
		# в словаре информацию о значениях аттрибутов по   #
		# умолчанию и выделять значением равным '?' аттри- #
		# буты для которых нужно искать значения в файле   #
		# JSON c исходными данными.						#
		####################################################

series_atrib_dic = {'FREQ': 'A', 'TAX_KIND': '?', 'TIME_PERIOD': '2018'}
series_atrib_maper = {'TAX_KIND': 'id'}

		####################################################
		# Работа с тегом Obs							   #
		# 												   #
		# Тк при конвертации из JSON в XML происходит уве- # 
		# лечение размерности данных - нужно явно указать  #
		# по каким полям будет генерация тегов Obs.		   #
		#												   #
		# obs_list - список полей записи JSON для создания #
		#			серии тегов Obs					       #
		#												   #
		# obs_atrib_dic - словарь аттрибутов каждого тега  #
		#				 Obs. Виесто знака '§' подставля-  #
		#				 ется значение из obs_list		   #
		####################################################

obs_list = ['accrued', 'consolidated', 'enrolled', 'federal']
obs_atrib_dic = {'OBS_VALUE': '?', 'UNIT_MEASURE': 'THS', 'type': '§'}

		# Сдлварь для записи значение obs_list в стиле XML
obs_atrib_maper = {  'accrued': 'ACCRUED', 
					 'consolidated': 'CONSOLIDATED', 
					 'enrolled': 'ENROLLED', 
					 'federal': 'FEDERAL'}

prep_data_dic = convert_JSON2metaJSON(  raw_data_dic, 
										temp_data_dic, 
					  					series_atrib_dic, 
					  					series_atrib_maper,
					  					obs_list,
					  					obs_atrib_dic,
					  					obs_atrib_maper )

fl.write_json('./data/output/prep_data_01.json', prep_data_dic)

		####################################################
		#  СОЗДАНИЕ МОДЕЛИ ДОКУМЕНТА XML				   #
		#						   						   #
		#  Создание корневого тега и основных сегментов бу-#
		#  дущего XML документа.						   #
		####################################################

		# Создание qname корневого тега 
structure_qname = ET.QName(ns_dic['message'], 'Structure')

		# Создание модели будущего XML документа
dm = Document_model(structure_qname, ns_dic)

		# Создание двух сегметнов будущего XML документа   
dm.create_segment('Header', 'message', 'Structure', 'message')
dm.create_segment('DataSet', 'message', 'Structure', 'message')

		# Ссылка на node корневого тега
root = dm.get_root()

		####################################################
		#  ЗАПОЛНЕНИЕ СЕГМЕНТОВ ДОКУМЕНТА XML			   #
		#						   						   #
		#  Происходит поиск по имени нужного сегмента, по  #
		#  metaJSON просходит создание ET.elemnt и рекур-  #
		#  сивное добавление к корню.					   #
		####################################################

generate_ET_from_JSON(root, header_dic, 'Header', ns_dic)
generate_ET_from_JSON(root, prep_data_dic, 'DataSet', ns_dic, False)

		# Записываем модель документа в XML-файл
dm.write('./data/output/data_01.sdmx.xml')

