def _get_fields(attrs):
    fields = {}
    for field_name, field_val in attrs.items():
        if not field_name.startswith('__'):
            fields[field_name] = field_val
    return fields


def _get_default_dict(_fields):
    def_dict = {}
    for field, field_ins in _fields.items():
        def_dict[field] = field_ins.default
    return def_dict


def _is_primary_field(model, field_name):
    return model.__fields__[field_name].primary_key


def __set_fields__(attr_dict):
    fields = {}
    for field, value in attr_dict.items():
        pass
        # if isinstance(value, Field) and value.foreign_key == False:
        #     cls.__fields__[key] = value
        #     cls.__fields__[key].name = '{}.{}'.format(cls.__table_name__, key)
        #     cls.__fields__[key].short_name = key
        #     if value.default:
        #         fields[key] = value.default
        # elif isinstance(value, Field) and value.foreign_key == True:
        #     cls.__fields__['foreign_key'] = value
    return fields