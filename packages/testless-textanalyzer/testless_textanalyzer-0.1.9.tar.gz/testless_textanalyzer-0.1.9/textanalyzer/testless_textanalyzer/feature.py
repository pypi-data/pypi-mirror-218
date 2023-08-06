from collections import Counter, defaultdict

import numpy as np


STARTING_TOKEN = '*'        # Label of t=-1
STARTING_TOKEN_INDEX = 0


class FeatureSet():
    def __init__(self):
        # Sets a custom feature function.
        self.feature_dic = defaultdict(dict)
        self.observation_set = set()
        self.empirical_counts = Counter()
        self.num_features = 0

        self.label_dic = {STARTING_TOKEN: STARTING_TOKEN_INDEX}
        self.label_array = [STARTING_TOKEN]

        self.feature_func =  self.word2features

    def word2features(self, X, i):
        """
        Returns a list of feature strings.
        :param X: An observation vector (word, pos_tag, ner_tag)
        :param i: time
        :return: A list of feature strings
        """
        features = []
        word, pos_tag = X[i][:2]

        # Current word and POS features
        features.append(f'U[0]:{word}')
        features.append(f'POS_U[0]:{pos_tag}')

        if i < len(X) - 1:
            next_word, next_pos_tag = X[i + 1][:2]

            # Next word and POS features
            features.append(f'U[+1]:{next_word}')
            features.append(f'B[0]:{word} {next_word}')
            features.append(f'POS_U[1]:{next_pos_tag}')
            features.append(f'POS_B[0]:{pos_tag} {next_pos_tag}')

            if i < len(X) - 2:
                next_next_word, next_next_pos_tag = X[i + 2][:2]

                # Next next word and POS features
                features.append(f'U[+2]:{next_next_word}')
                features.append(f'POS_U[+2]:{next_next_pos_tag}')
                features.append(f'POS_B[+1]:{next_pos_tag} {next_next_pos_tag}')
                features.append(f'POS_T[0]:{pos_tag} {next_pos_tag} {next_next_pos_tag}')

        if i > 0:
            prev_word, prev_pos_tag = X[i - 1][:2]

            # Previous word and POS features
            features.append(f'U[-1]:{prev_word}')
            features.append(f'B[-1]:{prev_word} {word}')
            features.append(f'POS_U[-1]:{prev_pos_tag}')
            features.append(f'POS_B[-1]:{prev_pos_tag} {pos_tag}')

            if i < len(X) - 1:
                next_pos_tag = X[i + 1][1]

                # Previous and current POS tag features
                features.append(f'POS_T[-1]:{prev_pos_tag} {pos_tag} {next_pos_tag}')

            if i > 1:
                prev_prev_word, prev_prev_pos_tag = X[i - 2][:2]

                # Previous previous word and POS features
                features.append(f'U[-2]:{prev_prev_word}')
                features.append(f'POS_U[-2]:{prev_prev_pos_tag}')
                features.append(f'POS_B[-2]:{prev_prev_pos_tag} {prev_pos_tag}')
                features.append(f'POS_T[-2]:{prev_prev_pos_tag} {prev_pos_tag} {pos_tag}')

        return features


    def constract_X_Y(self, data):
        """
        Constructs a feature set, a label set,
            and a counter of empirical counts of each feature from the input data.
        :param data: A list of (X, Y) pairs. (X: observation vector , Y: label vector)
        """
        # Constructs a feature set, and counts empirical counts.
        for X, Y in data:
            prev_y = STARTING_TOKEN_INDEX
            for t in range(len(X)):
                # Gets a label id
                try:
                    y = self.label_dic[Y[t]]
                except KeyError:
                    y = len(self.label_dic)
                    self.label_dic[Y[t]] = y
                    self.label_array.append(Y[t])
                # Adds features
                self.add_feature(prev_y, y, X, t)
                prev_y = y

    def load(self, feature_dic, num_features, label_array):
        self.num_features = num_features
        self.label_array = label_array
        self.label_dic = {label: i for label, i in enumerate(label_array)}
        self.feature_dic = self.deserialize_feature_dict(feature_dic)

    def __len__(self):
        return self.num_features

    def add_feature(self, prev_label, current_label, observation_vector, time):
        """
        Adds features and updates the feature dictionary.
        :param prev_label: Previous label
        :param current_label: Current label
        :param observation_vector: Observation vector X
        :param time: Time
        """
        feature_strings = self.feature_func(observation_vector, time)

        for feature_string in feature_strings:
            if feature_string not in self.feature_dic:
                self.feature_dic[feature_string] = {}

            # Update counts and feature dictionary for (prev_label, current_label)
            if (prev_label, current_label) in self.feature_dic[feature_string]:
                feature_id = self.feature_dic[feature_string][(prev_label, current_label)]
                self.empirical_counts[feature_id] += 1
            else:
                feature_id = self.num_features
                self.feature_dic[feature_string][(prev_label, current_label)] = feature_id
                self.empirical_counts[feature_id] += 1
                self.num_features += 1

            # Update counts and feature dictionary for (-1, current_label)
            if (-1, current_label) in self.feature_dic[feature_string]:
                feature_id = self.feature_dic[feature_string][(-1, current_label)]
                self.empirical_counts[feature_id] += 1
            else:
                feature_id = self.num_features
                self.feature_dic[feature_string][(-1, current_label)] = feature_id
                self.empirical_counts[feature_id] += 1
                self.num_features += 1


    def get_labels(self):
        """
        :return: a label dictionary and array.
        """
        return self.label_dic, self.label_array


    def calc_inner_products(self, params, X, t):
        """
        Calculates inner products of the given parameters and feature vectors of the given observations at time t.
        :param params: parameter vector
        :param X: observation vector
        :param t: time
        :return: list of tuples containing inner product pairs and scores
        """
        inner_products = []
        feature_strings = self.feature_func(X, t)
        
        for feature_string in feature_strings:
            if feature_string in self.feature_dic:
                feature_dict = self.feature_dic[feature_string]
                prev_y_values, y_values = zip(*feature_dict.keys())
                feature_ids = list(feature_dict.values())

                inner_product_scores = params[feature_ids]
                inner_product_pairs = list(zip(prev_y_values, y_values))
                
                inner_products.extend(zip(inner_product_pairs, inner_product_scores))
        
        return inner_products

    def get_empirical_counts(self):
        """
        Retrieves the empirical counts of features and returns them as a NumPy array.
        :return: NumPy array of empirical counts
        """
        empirical_counts = np.zeros((self.num_features,))
        feature_ids = list(self.empirical_counts.keys())
        counts = list(self.empirical_counts.values())
        empirical_counts[feature_ids] = counts
        return empirical_counts

    def get_feature_list(self, X, t):
        """""
        :return: a list of feature ids and a list of feature strings.
        """""
        feature_list_dic = defaultdict(set)
        for feature_string in self.feature_func(X, t):
            for (prev_y, y), feature_id in self.feature_dic[feature_string].items():
                feature_list_dic[(prev_y, y)].add(feature_id)
        return [((prev_y, y), feature_ids) for (prev_y, y), feature_ids in feature_list_dic.items()]

    def serialize_feature_dict(self):
        """""
        : return: a serialized feature dictionary (a dictionary of dictionaries)
        """""
        serialized = {
            feature_string: {
                f'{prev_label}_{current_label}': feature_id
                for (prev_label, current_label), feature_id in feature_dict.items()
            }
            for feature_string, feature_dict in self.feature_dic.items()
        }
        return serialized
    
    def deserialize_feature_dict(self, serialized):
        """""
        : return: a deserialized feature dictionary (a dictionary of dictionaries)
        """""
        feature_dict = {
            feature_string: {
                tuple(map(int, transition_string.split('_'))): feature_id
                for transition_string, feature_id in transition_dict.items()
            }
            for feature_string, transition_dict in serialized.items()
        }
        return feature_dict
