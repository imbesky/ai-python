import calendar
import csv
import numbers
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer0
        - Administrative_Duration, a floating point number1
        - Informational, an integer2
        - Informational_Duration, a floating point number3
        - ProductRelated, an integer4
        - ProductRelated_Duration, a floating point number5
        - BounceRates, a floating point number6
        - ExitRates, a floating point number7
        - PageValues, a floating point number8
        - SpecialDay, a floating point number9
        - Month, an index from 0 (January) to 11 (December)10
        - OperatingSystems, an integer11
        - Browser, an integer12
        - Region, an integer13
        - TrafficType, an integer14
        - VisitorType, an integer 0 (not returning) or 1 (returning)15
        - Weekend, an integer 0 (if false) or 1 (if true)16

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    months = {
        m[:3]: i for i, m in enumerate(calendar.month_abbr)
    }

    def evidence_list(data):
        e = [int(data[0]), float(data[1]), int(data[2]), float(data[3]), int(data[4])]
        for i in range(5, 10):
            e.append(float(data[i]))
        e.append(months[data[10][:3]] - 1)
        for i in range(11, 15):
            e.append(int(data[i]))
        if data[15] == "Returning_Visitor":
            e.append(1)
        else:
            e.append(0)
        if data[16] == "FALSE":
            e.append(0)
        elif data[16] == "TRUE":
            e.append(1)
        return e

    evidences = []
    results = []
    with open('shopping.csv') as csv_file:
        datas = csv.reader(csv_file, delimiter=',')
        next(datas, None)
        for row in datas:
            evidences.append(evidence_list(row))
            if row[17] == "FALSE":
                results.append(0)
            elif row[17] == "TRUE":
                results.append(1)
    return evidences, results


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(evidence, labels)
    return classifier


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    predict_p = 0.0
    actual_and_predict_p = 0.0
    predict_n = 0.0
    actual_and_predict_n = 0.0
    for i in range(len(labels)):
        if predictions[i] == 1:
            predict_p += 1
            if labels[i] == 1:
                actual_and_predict_p += 1
        elif predictions[i] == 0:
            predict_n += 1
            if labels[i] == 0:
                actual_and_predict_n += 1
    sensitivity = actual_and_predict_p / predict_p
    specificity = actual_and_predict_n / predict_n
    return sensitivity, specificity


if __name__ == "__main__":
    main()
