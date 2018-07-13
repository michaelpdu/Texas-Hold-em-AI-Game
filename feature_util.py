import collections

max_dim_index = 200

def convert_to_libsvm_format(label, features, comments = ''):
    feature_msg = ''
    if isinstance(features, dict):
        ordered_features = collections.OrderedDict(sorted(features.items()))
        for i in ordered_features:
            value = ordered_features[i]
            if float(value) > 0:
                feature_msg += '{}:{} '.format(i, value)
    else:
        feature_msg = features

    return '{} {} {}:0 # {}\n'.format(label, feature_msg, max_dim_index, comments)