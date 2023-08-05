import numpy as np
from ete3 import Tree
from scipy.integrate import odeint
from treesimulator.mtbd_models import BirthDeathExposedInfectiousModel

from pybdei import parse_forest

RTOL = 100 * np.finfo(np.float64).eps
N_U_STEPS = int(1e7)

TIME = 'time'


def annotate_tree(tree):
    for n in tree.traverse('preorder'):
        if n.is_root():
            p_time = 0
        else:
            p_time = getattr(n.up, TIME)
        n.add_feature(TIME, p_time + n.dist)


def compute_U(T, MU, LA, PSI, RHO, SIGMA=None, nsteps=N_U_STEPS):
    """
    Calculates a function get_U which for a given time t: 0 <= t <= T, would return
    an array of unobserved probabilities [U_1(t), ..., U_m(t)].

    U_k(t) are calculated by
    (1) solving their ODEs numerically for an array tt of nsteps times equally spaced between t=T and t=0,
    producing an array of solutions sol of length nstep (for corresponding times in tt)s.
    (2) creating a linear approximation which for a given time t (2a) find an index i such that tt[i] >= t > tt[i+1];
    (2b) returns sol[i + 1] + (sol[i] - sol[i + 1]) * (tt[i] - t) / (tt[i] - tt[i + 1]).


    :param T: time at end of the sampling period
    :param MU: an array of state transition rates
    :param LA: an array of transmission rates
    :param PSI: an array of removal rates
    :param RHO: an array of sampling probabilities
    :param SIGMA: an array of rate sums: MU.sum(axis=1) + LA.sum(axis=1) + PSI
    :return: a function that for a given time t returns the array of corresponding unsampled probabilities:
        t ->  [U_1(t), ..., U_m(t)].
    """

    if SIGMA is None:
        SIGMA = MU.sum(axis=1) + LA.sum(axis=1) + PSI

    tt = np.linspace(T, 0, nsteps)
    y0 = np.ones(LA.shape[0], np.float64)
    PSI_NOT_RHO = PSI * (1 - RHO)

    def pdf_U(U, t):
        dU = (SIGMA - LA.dot(U)) * U - MU.dot(U) - PSI_NOT_RHO
        return dU

    sol = odeint(pdf_U, y0, tt, rtol=RTOL)
    sol = np.maximum(sol, 0)
    return sol


forest = parse_forest('/home/azhukova/projects/bdei_main/ebola/data/SLE/SLE.bottom.0.days.nwk')
for tree in forest:
    annotate_tree(tree)
T = max(max(getattr(_, TIME) for _ in tree) for tree in forest)

mu, la, psi, rho = 0.08888680840558337,	22.811375741946357,	22.746490323095674,	0.057186311787072244
model = BirthDeathExposedInfectiousModel(mu=mu, la=la, psi=psi, p=rho)
Us = compute_U(T, model.transition_rates, model.transmission_rates, model.removal_rates, model.ps)[-1]
U = model.state_frequencies.dot(Us)
u = len(forest) * U / (1 - U)
print(u)
