# NCAFS

_Neighborhood Component Analysis Feature Selection_

NCAFS is a non-parametric algorithm based on k-nearest neighbors (kNN), which learns a feature weighting 
vector by minimizing the expected leave-one-out error with a regularization term. NCA was originally 
proposed in [1], which inspired the feature selection method for classification presented in [2]. It was 
then extended to regression problems as well [3].

NCAFS is a Python package that implements the NCA feature selection method, for both classification and
regression problems.

## Instalation
```commandline
pip install ncafs
```

## Getting started

### Classification
```python
from ncafs import NCAFSC
from sklearn import datasets

X, y = datasets.make_classification(
    n_samples=1000,
    n_classes=5,
    n_features=20,
    n_informative=100,
    n_redundant=0,
    n_repeated=0,
    flip_y=0.1,
    class_sep=0.5,
    shuffle=False,
    random_state=0
)

fs_clf = NCAFSC()
fs_clf.fit(X, y)
w = fs_clf.weights_
```

### Regression
```python
from ncafs import NCAFSR
from sklearn import datasets

X, y, coef = datasets.make_regression(
    n_samples=1000,
    n_features=100,
    n_informative=20,
    bias=0,
    noise=1e-3,
    coef=True,
    shuffle=False,
    random_state=0
)

fs_reg = NCAFSR()
fs_reg.fit(X, y)
w = fs_reg.weights_
```

## References

1. Goldberger, J., Hinton, G., Roweis, S., Salakhutdinov, R. (2005). Neighbourhood Components Analysis. Advances in Neural Information Processing Systems. 17, 513-520.
2. Yang, W., Wang, K., & Zuo, W. (2012). Neighborhood component feature selection for high-dimensional data. J. Comput., 7(1), 161-168.
3. Amankwaa-Kyeremeh, B., Greet, C., Zanin, M., Skinner, W. and Asamoah, R. K., (2020), Selecting key
   predictor parameters for regression analysis using modified Neighbourhood Component Analysis (NCA)
   Algorithm. Proceedings of 6th UMaT Biennial International Mining and Mineral Conference, Tarkwa, Ghana,
   pp. 320-325.
