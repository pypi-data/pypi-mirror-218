#!/usr/bin/env python3
"""Fermi-orbital descriptor generation."""
import numpy as np
from scipy.linalg import norm

from ..data import SYMBOL2NUMBER
from ..logger import log
from ..units import bohr2ang


def get_localized_orbitals(mf, Nspin, loc, Nit=1000, seed=1234):
    """Generate localized orbitals with an additional simple stability analysis.

    Same as implemented in PyFLOSIC2.

    Reference: J. Chem. Phys. 153, 084104.

    Args:
        mf: PySCF SCF object.
        Nspin (int): Number of spin states.
        loc (str): Localization method (case insensitive).

    Keyword Args:
        Nit (int): Number of tries to get a solution with positive eigenvalues.
        seed (int): Seed to initialize the random number generator.

    Returns:
        list: Localized occupied orbital coefficients per spin channel.
    """
    rng = np.random.default_rng(seed=seed)
    from pyscf.lo import boys, edmiston, pipek
    loc_dict = {'ER': edmiston.EdmistonRuedenberg,
                'FB': boys.Boys,
                'GPM': pipek.PipekMezey,
                'PM': pipek.PipekMezey}

    loc_orb = []
    # Localize each spin channel separately
    for s in range(Nspin):
        # Initialize the localizer object
        if Nspin == 2:
            localizer = loc_dict[loc](mf.mol, mf.mo_coeff[s][:, mf.mo_occ[s] > 0])
        else:
            localizer = loc_dict[loc](mf.mol, mf.mo_coeff[:, mf.mo_occ > 0])

        # Set the population method in generalized PM to Becke charges
        if loc == 'GPM':
            localizer.pop_method = 'becke'

        for _ in range(Nit):
            tmp_orb = localizer.kernel()
            # Calculate the eigenvalues of the Hessian
            _, _, h_diag = localizer.gen_g_hop(u=np.eye(len(tmp_orb[0])))
            # If there are no eigenvalues or all of them are positive break the loop
            if len(h_diag) == 0 or np.min(h_diag) > 0:
                break
            # If not continue with randomly 'displaced' orbitals
            noise = rng.normal(scale=5e-4, size=tmp_orb.shape)
            localizer.mo_coeff = tmp_orb + noise
        loc_orb.append(tmp_orb)
    return loc_orb


def get_fods(object, basis='pc-1', loc='FB', elec_symbols=None):
    """Generate FOD positions using the PyCOM method.

    Reference: J. Comput. Chem. 40, 2843.

    Args:
        object: Atoms or SCF object.

    Keyword Args:
        basis (str): Basis set for the DFT calculation.
        loc (str): Localization method (case insensitive).
        elec_symbols (list): Identifier for up and down FODs.

    Returns:
        ndarray: FOD positions.
    """
    try:
        from pyscf.gto import Mole
        from pyscf.scf import RKS, UKS
    except ImportError:
        log.exception('Necessary dependencies not found. To use this module, '
                      'install them with "pip install eminus[fods]".\n\n')
        raise

    try:
        atoms = object.atoms
    except AttributeError:
        atoms = object
    loc = loc.upper()

    if elec_symbols is None:
        elec_symbols = ('X', 'He')
        if 'He' in atoms.atom and atoms.Nspin == 2:
            log.warning('You need to modify "elec_symbols" to calculate helium in the spin-'
                        'polarized case.')

    # Convert to Angstrom for PySCF
    X = bohr2ang(atoms.X)
    # Build the PySCF input format
    atom_pyscf = list(zip(atoms.atom, X))

    # Spin in PySCF is the difference of up and down electrons
    if atoms.Nspin == 2:
        spin = int(np.sum(atoms.f[0] - atoms.f[1]))
    else:
        spin = int(np.sum(atoms.Z) % 2)

    # Do the PySCF DFT calculation
    # Use Mole.build() over M() since the parse_arg option breaks testing with pytest
    mol = Mole(atom=atom_pyscf, basis=basis, spin=spin).build(parse_arg=False)
    if atoms.Nspin == 1:
        mf = RKS(mol=mol)
    else:
        mf = UKS(mol=mol)
    mf.verbose = 0
    mf.kernel()

    # Get the localized orbital coefficients
    loc_orb = get_localized_orbitals(mf, atoms.Nspin, loc)
    # Calculate the COMs
    loc_com = []
    ao = mf._numint.eval_ao(mf.mol, mf.grids.coords)
    for s in range(atoms.Nspin):
        phi = ao @ loc_orb[s]
        dens = phi.conj() * phi * mf.grids.weights[:, None]
        loc_com.append(dens.T @ mf.grids.coords)
    return loc_com


def split_fods(atom, X, elec_symbols=None):
    """Split atom and FOD coordinates.

    Args:
        atom (list): Atom symbols.
        X (ndarray): Atom positions.

    Keyword Args:
        elec_symbols (list): Identifier for up and down FODs.

    Returns:
        tuple[list, ndarray, list]: Atom types, the respective coordinates, and FOD positions.
    """
    if elec_symbols is None:
        elec_symbols = ('X', 'He')

    X_fod_up = []
    X_fod_dn = []
    # Iterate in reverted order, because we may delete elements
    for ia in range(len(X) - 1, -1, -1):
        if atom[ia] in elec_symbols:
            if atom[ia] in elec_symbols[0]:
                X_fod_up.append(X[ia])
            if len(elec_symbols) > 1 and atom[ia] in elec_symbols[1]:
                X_fod_dn.append(X[ia])
            X = np.delete(X, ia, axis=0)
            del atom[ia]

    X_fod = [np.asarray(X_fod_up), np.asarray(X_fod_dn)]
    return atom, X, X_fod


def remove_core_fods(object, fods):
    """Remove core FODs from a set of FOD coordinates.

    Args:
        object: Atoms or SCF object.
        fods (list): FOD positions.

    Returns:
        ndarray: Valence FOD positions.
    """
    try:
        atoms = object.atoms
    except AttributeError:
        atoms = object

    # If the number of valence electrons is the same as the number of FODs, do nothing
    if atoms.Nspin == 1 and len(fods[0]) * 2 == np.sum(atoms.f[0]):
        return fods
    if atoms.Nspin == 2 and len(fods[0]) == np.sum(atoms.f[0]) \
            and len(fods[1]) == np.sum(atoms.f[1]):
        return fods

    for s in range(atoms.Nspin):
        for ia in range(atoms.Natoms):
            n_core = SYMBOL2NUMBER[atoms.atom[ia]] - atoms.Z[ia]
            # In the spin-paired case two electrons are one state
            # Since only core states are removed in pseudopotentials this value is divisible by 2
            # +1 to account for uneven amount of core FODs (e.g., for hydrogen)
            n_core = (n_core + 1) // 2
            dist = norm(fods[s] - atoms.X[ia], axis=1)
            idx = np.argsort(dist)
            # Remove core FODs with the smallest distance to the core
            fods[s] = np.delete(fods[s], idx[:n_core], axis=0)
    return fods
