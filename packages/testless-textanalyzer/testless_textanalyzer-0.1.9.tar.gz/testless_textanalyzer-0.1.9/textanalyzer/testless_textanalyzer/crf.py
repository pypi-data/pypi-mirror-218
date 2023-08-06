from textanalyzer.testless_textanalyzer.read_data import read_data
from textanalyzer.testless_textanalyzer.feature import FeatureSet, STARTING_TOKEN_INDEX
import numpy as np
from scipy.optimize import fmin_l_bfgs_b
from textanalyzer.testless_textanalyzer.crf_utils import calculate_log_likelihood, _gradient, _generate_potential_table
from tqdm import tqdm

import time
import datetime
import pickle
import os


class LinearChainCRF:
    def __init__(self):
        self.training_data = None
        self.feature_set = None
        self.label_dic = None
        self.label_array = None
        self.num_labels = None
        self.params = None
        self.squared_sigma = 10.0

    def _read_data(self, filename):
        return read_data(filename)

    def _get_training_feature_data(self):
        return [
            [self.feature_set.get_feature_list(X, t) for t in range(len(X))]
            for X, _ in self.training_data
        ]

    def _estimate_parameters(self, maxiter=100):
        training_feature_data = self._get_training_feature_data()
        print('   ========================')
        pbar = tqdm(total=maxiter)  # Initialize tqdm with the total number of iterations

        def update_progress(xk):  # Define a callback function to update tqdm
            pbar.update(1)  # Increment the progress bar by 1

        self.params, log_likelihood, information = fmin_l_bfgs_b(
            func=calculate_log_likelihood,
            fprime=_gradient,
            x0=np.zeros(len(self.feature_set)),
            args=(
                self.training_data,
                self.feature_set,
                training_feature_data,
                self.feature_set.get_empirical_counts(),
                self.label_dic,
                self.squared_sigma,
            ),
            callback=update_progress,  # Pass the callback function to update the progress bar
            maxiter=maxiter,
        )
        pbar.close()  # Close the tqdm progress bar
        print('   ========================')
        print('* Training has been finished with %d iterations' % information['nit'])

        if information['warnflag'] != 0:
            print('* Warning (code: %d)' % information['warnflag'])
            if 'task' in information.keys():
                print('* Reason: %s' % (information['task']))
        print('* Likelihood: %s' % str(log_likelihood))


    def train(self, corpus_filename, model_filename, maxiter=100):
        start_time = time.time()
        print('[%s] Start training' % datetime.datetime.now())

        print("* Reading training data ... ", end="")
        self.training_data = self._read_data(corpus_filename)
        print("Done")

        self.feature_set = FeatureSet()
        self.feature_set.constract_X_Y(self.training_data)
        self.label_dic, self.label_array = self.feature_set.get_labels()
        self.num_labels = len(self.label_array)
        print("* Number of labels: %d" % (self.num_labels - 1))
        print("* Number of features: %d" % len(self.feature_set))

        self._estimate_parameters(maxiter=maxiter)

        self.save_model(model_filename)

        elapsed_time = time.time() - start_time
        print('* Elapsed time: %f' % elapsed_time)
        print('* [%s] Training done' % datetime.datetime.now())

    def test(self, test_corpus_filename):
        if self.params is None:
            raise BaseException("the model should be trained first")

        test_data = self._read_data(test_corpus_filename)
        y_pred = []
        y_true = []
        
        for X, Y in test_data:
            Yprime = self.inference(X)
            y_pred.append(Yprime)
            y_true.append(Y)

        return y_pred, y_true

    def predict(self, test_data):
        if self.params is None:
            raise BaseException("the model should be trained first")

        y_pred = []

        for X in test_data:
            Yprime = self.inference(X)
            y_pred.append(Yprime)

        return y_pred

    def inference(self, X):
        potential_table = _generate_potential_table(self.params, self.num_labels, self.feature_set, X, inference=True)
        y_predict = self.viterbi(X, potential_table)
        return y_predict

    def viterbi(self, X, potential_table):
        time_length = len(X)
        max_table = np.zeros((time_length, self.num_labels))
        argmax_table = np.zeros((time_length, self.num_labels), dtype='int64')

        potential_table = np.array(potential_table)

        max_table[0] = potential_table[0, STARTING_TOKEN_INDEX, :]

        for t in range(1, time_length):
            max_table[t] = np.max(max_table[t - 1, :, None] * potential_table[t], axis=0)
            argmax_table[t] = np.argmax(max_table[t - 1, :, None] * potential_table[t], axis=0)

        sequence = [np.argmax(max_table[-1])]
        for t in range(time_length - 1, 0, -1):
            sequence.append(argmax_table[t, sequence[-1]])
        sequence.reverse()

        return [self.label_dic[label_id] for label_id in sequence]

    def save_model(self, model_filename):
        model = {
            "feature_dic": self.feature_set.serialize_feature_dict(),
            "num_features": self.feature_set.num_features,
            "labels": self.feature_set.label_array,
            "params": list(self.params),
        }
        with open('Text_Analyzer/model/'+model_filename + '.pkl', 'wb') as f:
            pickle.dump(model, f)
        print(f'* Trained CRF Model has been saved at "{os.getcwd()}Text_Analyzer/model/{model_filename}"')

    def load(self, model_filename):
        with open(model_filename + '.pkl', 'rb') as f:
            model = pickle.load(f)

        self.feature_set = FeatureSet()
        self.feature_set.load(model['feature_dic'], model['num_features'], model['labels'])
        self.label_dic, self.label_array = self.feature_set.get_labels()
        self.num_labels = len(self.label_array)
        self.params = np.asarray(model['params'])

        print('CRF model loaded ...')
