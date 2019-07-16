from lxml import etree as ET

class Document_model:
	"""Класс для реализации модели документа XML.

	Реализован на основе библиотеки 'lxml'. Прелоставляет
	добавление сегментов, поиск сегментов и запись в файл.

	Attributes
	----------
	ns_map : dict
		Хранит в себе словарь пространства имен данного документа.
	root : :obj: ET.Element
		Хранит в себе корневой тег.

	"""
	def __init__(self, root_qname, ns_map):
		self.ns_map = ns_map
		self.root = ET.Element(root_qname, nsmap=ns_map)

	def get_root(self):
		"""Обращение к корневому тегу.

		Returns
		-------
		obj: ET.Element
			Корень 'lxml.etree'.

		"""
		return self.root

	def get_segment(self, segment_name, segment_ns_value):
		"""Обращение к заглавному тегу сегмента.

		Parameters
		----------
		segment_name
			Имя сегмента.
		segment_ns_value
			Пространство имен к которому принадлежит тег.

		Returns
		-------
		obj: ET.Element
			Элемент 'lxml.etree'.

		"""
		full_name = '{0}{1}'.format('{' + self.ns_map[segment_ns_value] + '}', segment_name) 
		return self.root.find(full_name)

	def create_segment(self, segment_name, segment_ns_value, perent_segment_name, perent_segment_ns_value, segment_children = False):
		"""Создание новго сегмента в модели.

		Происходит только создание заглавного тега сегмента. Заполнение сегмента
		происходит в 'generator'. Возможно заполнение дочерними эдемнтами простой 
		структуры передаваемых в 'segment_children'.

		Parameters
		----------
		segment_name
			Имя сегмента.
		segment_ns_value
			Пространство имен к которому принадлежит тег.
		perent_segment_name
			Имя родительского тега к которому будет добавлен новый сегмент.
		perent_segment_ns_value
			Пространство имен к которому принадлежит родительский тег.
		segment_children : dict
			Словарь дочерних элементов с простой структурой нового сегмента. 
			В словаре ключ - имя XML тега, значение - значение XML тега. 

		Returns
		-------
		bool
			True if successful, False otherwise.

		"""
		segment_qname = ET.QName(self.ns_map[segment_ns_value], segment_name)
		if (perent_segment_name == 'Structure' and perent_segment_ns_value == 'message'):
			segment_tag = ET.SubElement(self.root, segment_qname, nsmap=self.ns_map)
		else:
			perent_full_name = '{0}{1}'.format('{' + self.ns_map[perent_segment_ns_value] + '}', perent_segment_name) 
			segment_tag = ET.SubElement(self.root.find(perent_full_name), segment_qname, nsmap=self.ns_map)
		
		if (type(segment_children) != bool):
			for key, value in segment_children.items():
				print(key, value)
				ET.SubElement(segment_tag, ET.QName(self.ns_map[segment_ns_value], key), name='df', nsmap=self.ns_map).text = value

	def write(self, output_file_path):
		xml_document_tree = ET.ElementTree(self.root)
		xml_document_tree.write(output_file_path, xml_declaration=True, encoding='utf-8', method="xml")