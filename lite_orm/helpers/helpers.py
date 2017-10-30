def _get_model_fields(model):
    fields = {}
    for field_name, field_val in model.__dict__.items():
        if not field_name.startswith('__'):
            fields[field_name] = field_val
    return fields


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