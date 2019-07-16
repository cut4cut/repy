from lxml import etree as ET

def convert_JSON2metaJSON(	raw_dict,
						 	meta_dict,  
							series_atrib_dic, 
							series_atrib_maper,
							obs_list,
							obs_atrib_dic, 
							obs_atrib_maper ):
	"""Конвертирует JSON в metaJSON для последующей генерации XML.

	Конвертация происходит по правилам записанными в словарях и списках.
	В словарях хранится информаиция о том, какие должны быть аттрибуты у 
	XML документа или перевод из полей JSON в аттрибуты  XML документа.
	В списке хранится набор полей записи JSON из которых должны выделить 
	новую размерность данных: вложженость тегов XML.

	metaJSON - это JSON c метаинформаицей о своих полях: поле яыляется аттрибутом или
	значением XML тега.

	Parameters
	----------
	raw_dict
		Исходный JSON c данными.
	meta_dict
		Словарь в который рекурсивно будут добавляться записи JSON c метатегами.
	series_atrib_dic
		Словарь с информацией о значениях аттрибутов по умолчанию. Значение равное '?' 
		заменяется на значение из 'raw_dict'.
	series_atrib_maper
		Словарь с переводом имен аттрибутов XML-документа в имена полей JSON-файла.
	obs_list
		Список полей JSON-записи из которых должны выделитьновую новую 
		размерность данных.
	obs_atrib_dic
		Словарь с информацией о значениях аттрибутов по умолчанию. Значение равное '?' 
		заменяется на значение из 'raw_dict'. Значение равное '§' заменяется на 
		значение из 'obs_list'.
	obs_atrib_maper
		Словарь с переводом имен полей JSON-файла в имена XML тегов.

	Returns
	-------
	dict
		Словарь, хранящий в себе metaJSON.

	"""
	series_dict = {"Series":  {}}
	attribs_dict = {}

	for attrib_key, attrib_value in series_atrib_dic.items():
		if (attrib_value == '?'):
			attribs_dict[attrib_key] = str(raw_dict[series_atrib_maper[attrib_key]])
		else:
			attribs_dict[attrib_key] = attrib_value
			
	series_dict["Series"]["@"] = attribs_dict
	series_dict["Series"]['#'] = []
	
	for obs_item in obs_list:
		obs_dict = {'Obs': {'@':{}}}

		for obs_key, obs_value in obs_atrib_dic.items():
			# Записываем что измерели 
			if (obs_value == '§'):
				obs_dict['Obs']['@'][obs_key] = obs_atrib_maper[obs_item]
			# Записываем сколько измерили
			elif (obs_value == '?'):
				obs_dict['Obs']['@'][obs_key] = str(raw_dict[obs_item])
			# Записываем значения по умолчанию 
			else:
				obs_dict['Obs']['@'][obs_key] = obs_value

		series_dict['Series']['#'].append(obs_dict)
	
	meta_dict['#'].append(series_dict)
	
	for key, value in raw_dict.items():
		
		if(type(value) is list):
			for item in value:
				convert_JSON2metaJSON(item, meta_dict, series_atrib_dic, series_atrib_maper, obs_list, obs_atrib_dic, obs_atrib_maper)
	return meta_dict

def convert_JSON2ET(root, dictinory, parent_key, ns_dic):
	"""Конвертирует JSON в lxml.etree, добавляя теги к сегменту 'parent_key'.

	Рекурсивно проходит по JSON и генерирует теги XML по мета-записям в JSON.

	Parameters
	----------
	root
		Корень lxml.etree.
	dictinory
		Словарь/JSON-файл по которому происходит генерация.
	parent_key
		Название сегмента к которому будут добавляться lxml.etree.element, 
		сгенерированные по 'dictinory'.
	ns_dic
		Словарь с пространством имен всего XML документа.

	"""
	for key, value in dictinory.items():
		####################################################
		# Конструкция из if-elif-elif нужна в силу особен- #
		# остей работы ET.SubElement() и обращения по клю- #
		# чу в словаре. Можно убрать эти конструкции и	 #
		# сделать обработку на отдельный случаи с отствуем #
		# или присуствием мета-тегов '@', '$' и '~'.	   #
		##################################################
		if (type(value) is dict and '@' in value.keys() and '$' in value.keys()):
			if (':' in key):
				names_list = key.split(':')
				if('~' == names_list[0]):
					node_qname = ET.QName(names_list[1])
				else:
					node_qname = ET.QName(ns_dic[names_list[0]], names_list[1])
			else:
				node_qname = ET.QName(ns_dic['message'], key)
			if (':' in parent_key):
				parent_names_list = parent_key.split(':')
				parent_node = find_node_by_key(root, parent_names_list[1], ns_dic, ns_value=parent_names_list[0])
			else:
				parent_node = find_node_by_key(root, parent_key, ns_dic)
			ET.SubElement(parent_node, node_qname, value['@'], nsmap=ns_dic).text = value['$']
			
		elif (type(value) is dict and '@' in value.keys()):
			if (':' in key):
				names_list = key.split(':')
				if('~' == names_list[0]):
					node_qname = ET.QName(names_list[1])
				else:
					node_qname = ET.QName(ns_dic[names_list[0]], names_list[1])
			else:
				node_qname = ET.QName(ns_dic['message'], key)
			if (':' in parent_key):
				parent_names_list = parent_key.split(':')
				parent_node = find_node_by_key(root, parent_names_list[1], ns_dic, ns_value=parent_names_list[0])
			else:
				parent_node = find_node_by_key(root, parent_key, ns_dic)
			ET.SubElement(parent_node, node_qname, value['@'], nsmap=ns_dic)

		elif(type(value) is dict and '$' in value.keys()):
			if (':' in key):
				names_list = key.split(':')
				if('~' == names_list[0]):
					node_qname = ET.QName(names_list[1])
				else:
					node_qname = ET.QName(ns_dic[names_list[0]], names_list[1])
			else:
				node_qname = ET.QName(ns_dic['message'], key)
			if (':' in parent_key):
				parent_names_list = parent_key.split(':')
				parent_node = find_node_by_key(root, parent_names_list[1], ns_dic, ns_value=parent_names_list[0])
			else:
				parent_node = find_node_by_key(root, parent_key, ns_dic)
			ET.SubElement(parent_node, node_qname, nsmap=ns_dic).text = value['$']

		if (type(value) is dict):
			convert_JSON2ET(root, value, key, ns_dic)
		elif(type(value) is list):
			for item in value:
				convert_JSON2ET(root, item, parent_key, ns_dic)

def convert_JSON2ET_whithout_NS(root, dictinory, parent_key, ns_dic):
	"""Конвертирует JSON в 'lxml.etree', добавляя теги к сегменту 'parent_key'.

	Рекурсивно проходит по JSON и генерирует теги XML по мета-записям в JSON.

	Parameters
	----------
	root
		Корень 'lxml.etree'.
	dictinory
		Словарь/JSON-файл по которому происходит генерация.
	parent_key
		Название сегмента к которому будут добавляться lxml.etree.element, 
		сгенерированные по 'dictinory'.
	ns_dic
		Словарь с пространством имен всего XML документа.

	"""
	for key, value in dictinory.items():
		if (type(value) is dict and '@' in value.keys() and '$' in value.keys()):
			node_qname = ET.QName(key)
			parent_node = find_node_by_key(root, parent_key, ns_dic, ns_bool=False)
			ET.SubElement(parent_node, node_qname, value['@']).text = value['$']
			
		elif (type(value) is dict and '@' in value.keys()):
			node_qname = ET.QName(key)
			parent_node = find_node_by_key(root, parent_key, ns_dic, ns_bool=False)
			ET.SubElement(parent_node, node_qname, value['@'])

		elif(type(value) is dict and '$' in value.keys()):
			node_qname = ET.QName(key)
			parent_node = find_node_by_key(root, parent_key, ns_dic, ns_bool=False)
			ET.SubElement(parent_node, node_qname).text = value['$']

		if (type(value) is dict):
			convert_JSON2ET_whithout_NS(root, value, key, ns_dic)
		elif(type(value) is list):
			for item in value:
				convert_JSON2ET_whithout_NS(root, item, parent_key, ns_dic)

def find_node_by_key(root, key, ns_dic, ns_value='message', ns_bool=True):
	"""Поиск node по имени тега в 'lxml.etree'.

	Форматирует строку 'str' для последующего поиска при помощи стандартного
	метода '.findall(str)'. Поиск происходит с учетом простарнства имен,
	поэтому значение 'ns_value' по умолчанию 'message'.

	Parameters
	----------
	root
		Корень 'lxml.etree'.
	key
		Имя тега.
	ns_dic
		Словарь с пространством имен всего XML документа.
	ns_value
		Пространство имен в котором происходит поиск.
	ns_bool
		Флаг - выбор поиск с пространством имен или без него.

	Returns
	-------
	ET.Elemnt
		Элемент 'lxml.etree'.

	"""
	if (ns_bool == True):
		full_name = './/{0}{1}'.format('{' + ns_dic[ns_value] + '}', key)
	else:
		full_name = './/{0}'.format(key)

	return root.findall(full_name)[-1]
