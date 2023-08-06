import numpy as np
from textanalyzer.testless_textanalyzer.feature import  STARTING_TOKEN_INDEX


SCALING_THR = 1e250

GRADIENT = None

def _generate_potential_table(params, num_labels, feature_set, X, inference=True):
    """
    Generates a potential table using given observations.
        The potential table is a matrix that represents the potentials or scores associated with 
        transitioning from one label to another at each time step.
        
    potential_table[t][prev_y, y]
        := exp(inner_product(params, feature_vector(prev_y, y, X, t)))
        
        (where 0 <= t < len(X))
    """
    tables = list()
    for t in range(len(X)):
        table = np.zeros((num_labels, num_labels))
        if inference:
            inner_products = feature_set.calc_inner_products(params, X, t)
            prev_y_values, y_values, scores = zip(*[(prev_y, y, score) for (prev_y, y), score in inner_products])

            # Convert to arrays
            prev_y_values = np.array(prev_y_values)
            y_values = np.array(y_values)
            scores = np.array(scores)

            # Create boolean masks
            mask1 = (prev_y_values != -1) & (y_values < num_labels)
            mask2 = (prev_y_values == -1) & (y_values < num_labels)

            # Update table using vectorized operations and masks
            np.add.at(table, (prev_y_values[mask1], y_values[mask1]), scores[mask1])
            np.add.at(table, (slice(None), y_values[mask2]), scores[mask2])

        else:
            for (prev_y, y), feature_ids in X[t]:
                score = sum(params[fid] for fid in feature_ids)
                if prev_y == -1:
                    table[:, y] += score
                else:
                    table[prev_y, y] += score
        table = np.exp(table)
        
        if t == 0:
            table[STARTING_TOKEN_INDEX+1:] = 0
        else:
            table[:,STARTING_TOKEN_INDEX] = 0
            table[STARTING_TOKEN_INDEX,:] = 0
            
        tables.append(table)

    return tables


def _forward_backward(num_labels, time_length, potential_table):
    """
    Calculates alpha (forward terms), beta (backward terms), and Z (instance-specific normalization factor)
    with a scaling method (suggested by Rabiner, 1989).

    num_labels: int, number of labels
    time_length: int, length of the sequence
    potential_table: numpy array of shape (time_length, num_labels, num_labels), potential table

    returns:
    alpha: numpy array of shape (time_length, num_labels), forward terms
    beta: numpy array of shape (time_length, num_labels), backward terms
    Z: float, instance-specific normalization factor
    scaling_dic: dictionary, scaling coefficients for overflow handling
    """

    alpha = np.zeros((time_length, num_labels))
    scaling_dic = dict()

    # Initialize alpha at time t = 0
    alpha[0] = potential_table[0][STARTING_TOKEN_INDEX, :]

    scaling_time = None
    scaling_coefficient = 1.0  # Initialize to 1.0 instead of None
    overflow_occured = np.zeros(num_labels, dtype=bool)

    # Forward pass: calculate alpha
    for t in range(1, time_length):
        alpha[t] = np.dot(alpha[t - 1], potential_table[t])
        alpha_t_exceed_threshold = alpha[t] > SCALING_THR

        # Check if alpha[t] exceeds the scaling threshold and no previous overflow occurred
        if np.any(alpha_t_exceed_threshold) and not np.any(overflow_occured):
            scaling_time = t - 1
            scaling_coefficient = SCALING_THR
            overflow_occured = alpha_t_exceed_threshold
            scaling_dic[scaling_time] = scaling_coefficient

        # Divide alpha[t-1] by the scaling coefficient for overflow handling
        alpha[t - 1][overflow_occured] = alpha[t - 1][overflow_occured] / scaling_coefficient
        alpha[t][overflow_occured] = 0

    # Backward pass: calculate beta
    beta = np.zeros((time_length, num_labels))
    beta[time_length - 1] = 1.0

    for t in range(time_length - 2, -1, -1):
        beta[t] = np.dot(beta[t + 1], potential_table[t + 1].T)
        beta[t] /= scaling_dic.get(t, 1.0)  # Use .get() method to handle missing keys

    # Calculate instance-specific normalization factor Z
    Z = np.sum(alpha[time_length - 1])

    return alpha, beta, Z, scaling_dic

def calculate_log_likelihood(params, *args):
    """
    Calculate likelihood and gradient
    
    params: parameters to be optimized
    """

    # Unpack the arguments
    _, feature_set, training_feature_data, empirical_counts, label_dic, squared_sigma = args
    
    # Initialize variables
    expected_counts = np.zeros(len(feature_set))
    total_logZ = 0
    scaling_coeffs = []

    # Iterate over training feature data
    for X_features in training_feature_data:
        # Generate potential table
        potential_table = _generate_potential_table(params, len(label_dic), feature_set, X_features, inference=False)
        
        # Apply forward-backward algorithm to calculate alpha, beta, Z, and scaling coefficients
        alpha, beta, Z, scaling_dic = _forward_backward(len(label_dic), len(X_features), potential_table)
        
        # Update total logZ and scaling coefficients
        total_logZ += np.log(Z) + np.sum(np.log(list(scaling_dic.values())))
        scaling_coeffs.append(scaling_dic)

        # Calculate expected counts
        for t in range(len(X_features)):
            potential = potential_table[t]
            for (prev_y, y), feature_ids in X_features[t]:
                # Calculate transition probability
                prob = _calculate_transition_probability(prev_y, y, t, alpha, beta, scaling_dic, Z, potential)

                # Update expected counts
                for fid in feature_ids:
                    expected_counts[fid] += prob

    # Calculate likelihood
    likelihood = _calculate_likelihood(empirical_counts, params, total_logZ, squared_sigma)

    # Calculate gradients
    gradients = _calculate_gradients(empirical_counts, expected_counts, params, squared_sigma)

    # Store gradients in global variable
    global GRADIENT
    GRADIENT = gradients

    return -likelihood


def _calculate_transition_probability(prev_y, y, t, alpha, beta, scaling_dic, Z, potential):
    """
    Calculate transition probability
    """

    if prev_y == -1:
        if t in scaling_dic:
            prob = (alpha[t, y] * beta[t, y] * scaling_dic[t]) / Z
        else:
            prob = (alpha[t, y] * beta[t, y]) / Z
    elif t == 0:
        if prev_y != STARTING_TOKEN_INDEX:
            prob = 0
        else:
            prob = (potential[STARTING_TOKEN_INDEX, y] * beta[t, y]) / Z
    else:
        if prev_y == STARTING_TOKEN_INDEX or y == STARTING_TOKEN_INDEX:
            prob = 0
        else:
            prob = (alpha[t - 1, prev_y] * potential[prev_y, y] * beta[t, y]) / Z

    return prob


def _calculate_likelihood(empirical_counts, params, total_logZ, squared_sigma):
    """
    Calculate likelihood
    """

    likelihood = np.dot(empirical_counts, params) - total_logZ - np.sum(params ** 2) / (squared_sigma * 2)
    return likelihood


def _calculate_gradients(empirical_counts, expected_counts, params, squared_sigma):
    """
    Calculate gradients
    """

    gradients = empirical_counts - expected_counts - params / squared_sigma
    return gradients


def _gradient(params, *args):
    return GRADIENT * -1


