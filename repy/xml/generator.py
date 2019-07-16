from .convertor import convert_JSON2ET, convert_JSON2ET_whithout_NS

def generate_ET_from_JSON(root, dictinory, parent_key, ns_dic, ns_bool=True):
	"""В зависимости от ns_bool вызывает функцию по конвертации JSON в lxml.etree.

    Разница между 'convert_JSON2ET' и 'convert_JSON2ET_whithout_NS' в том что
    первая функция генерирует XML теги с пространством имен по умолчанию, 
    вторая функци генерирует XML теги без пространства имен.

    Такое разделение удобно, когда в одном XML докумнте нужны сегменты с тегами
    как с пространтвом имен, так и без него.

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
	ns_bool
		Флаг в зависимости от которого вызывается функция с работой пространтвом 
		имен или без него. По умолчанию принимает значение 'True'. 

    Returns
    -------
    bool
        True if successful, False otherwise.

    """
	if ns_bool:
		convert_JSON2ET(root, dictinory, parent_key, ns_dic)
	else:
		full_parent_key = '{0}{1}'.format('{' + ns_dic['message'] + '}', parent_key)
		convert_JSON2ET_whithout_NS(root, dictinory, full_parent_key, ns_dic)