import sys
import os
import pandas as pd

sys.path.append("../src/")
import pytest
import src.pypontem.utils.unit_conversion as units


def test_pressure_conversions():
    p = units.UnitConversion.Pressure(500, "psia")
    p_pa = p.convert(to_unit="pa")
    p_psig = p.convert(to_unit="psig")
    p_bar = p.convert(to_unit="bar")
    p_barg = p.convert(to_unit="barg")
    assert round(p_pa, 1) == pytest.approx(3447378.6)
    assert round(p_psig, 1) == pytest.approx(485.3)
    assert round(p_bar, 2) == pytest.approx(34.47)
    assert round(p_barg, 2) == pytest.approx(33.46)

    # p_pa = units.UnitConversion.Pressure(3447378.6, "pa")
    # p_psia = p_pa.convert(to_unit="psia")
    # p_bar = p_pa.convert(to_unit="barg")

    # assert round(p_psia, 1) == pytest.approx(500)
    # assert round(p_bar, 2) == pytest.approx(34.47)


def test_flowrate_conversions():
    q = units.UnitConversion.LiquidFlowRate(1000, "m3_s")
    q_bbld = q.convert(to_unit="bbl_d")
    q_ft3s = q.convert(to_unit="ft3_s")
    q_bblh = q.convert(to_unit="bbl_h")
    q_gpm = q.convert(to_unit="gpm")
    q_lm = q.convert(to_unit="l_min")

    assert round(q_bbld, 1) == pytest.approx(543439650.5)
    assert round(q_ft3s, 1) == pytest.approx(35314.7)
    assert round(q_bblh, 1) == pytest.approx(22643318.7)
    assert round(q_gpm, 1) == pytest.approx(15850323.1)
    assert round(q_lm, 1) == pytest.approx(59999999.9)

    q_bbld = units.UnitConversion.LiquidFlowRate(543439650.5, "bbl_d")
    q_m3s = q_bbld.convert(to_unit="m3_s")
    q_ft3s = q_bbld.convert(to_unit="ft3_s")
    q_bblh = q_bbld.convert(to_unit="bbl_h")
    q_gpm = q_bbld.convert(to_unit="gpm")
    q_lm = q_bbld.convert(to_unit="l_min")

    assert round(q_m3s, 1) == pytest.approx(1000)
    assert round(q_ft3s, 1) == pytest.approx(35314.7)
    assert round(q_bblh, 1) == pytest.approx(22643318.7)
    assert round(q_gpm, 1) == pytest.approx(15850323.1)
    assert round(q_lm, 1) == pytest.approx(59999999.9)


def test_viscosity_conversions():
    mu = units.UnitConversion.DynamicViscosity(100, "cp")
    mu_pas = mu.convert(to_unit="pas")
    mu_lbfth = mu.convert(to_unit="lb_fth")
    mu_kgmh = mu.convert(to_unit="kg_mh")
    mu_nsm2 = mu.convert(to_unit="ns_m2")
    mu_kgms = mu.convert(to_unit="kg_ms")
    assert round(mu_pas, 1) == pytest.approx(0.1)
    assert round(mu_lbfth, 1) == pytest.approx(241.9)
    assert round(mu_kgmh) == pytest.approx(360)
    assert round(mu_nsm2, 1) == pytest.approx(0.1)
    assert round(mu_kgms, 1) == pytest.approx(0.1)

    mu_pas = units.UnitConversion.DynamicViscosity(0.1, "pas")
    mu_cp = mu_pas.convert(to_unit="cp")
    mu_lbfth = mu_pas.convert(to_unit="lb_fth")
    mu_kgmh = mu_pas.convert(to_unit="kg_mh")
    mu_nsm2 = mu_pas.convert(to_unit="ns_m2")

    assert round(mu_cp, 1) == pytest.approx(100)
    assert round(mu_lbfth, 1) == pytest.approx(241.9)
    assert round(mu_kgmh) == pytest.approx(360)
    assert round(mu_nsm2, 1) == pytest.approx(0.1)


def test_area_conversions():
    a_m2 = units.UnitConversion.Area(100, "m2")
    a_cm2 = a_m2.convert(to_unit="cm2")
    a_ft2 = a_m2.convert(to_unit="ft2")
    a_in2 = a_m2.convert(to_unit="in2")
    a_ft2 = a_m2.convert(to_unit="ft2")
    a_in2 = a_m2.convert(to_unit="in2")

    assert round(a_cm2, 1) == pytest.approx(1000000)
    assert round(a_ft2, 1) == pytest.approx(1076.4)
    assert round(a_in2, 1) == pytest.approx(155000.3)
    assert round(a_ft2, 1) == pytest.approx(1076.4)
    assert round(a_in2, 1) == pytest.approx(155000.3)


def test_density_conversions():
    rho_gcc = units.UnitConversion.Density(1, "g_cm3")
    rho_kgm3 = rho_gcc.convert(to_unit="kg_m3")
    rho_lbft3 = rho_gcc.convert(to_unit="lb_ft3")
    rho_lbin3 = rho_gcc.convert(to_unit="lb_in3")

    assert round(rho_kgm3, 1) == pytest.approx(1000)
    assert round(rho_lbft3, 1) == pytest.approx(62.4)
    assert round(rho_lbin3, 3) == pytest.approx(0.036)

    rho_kgm3 = units.UnitConversion.Density(1000, "kg_m3")
    rho_gcc = rho_kgm3.convert(to_unit="g_cm3")
    rho_lbft3 = rho_kgm3.convert(to_unit="lb_ft3")
    rho_lbin3 = rho_kgm3.convert(to_unit="lb_in3")

    assert round(rho_gcc, 1) == pytest.approx(1)
    assert round(rho_lbft3, 1) == pytest.approx(62.4)
    assert round(rho_lbin3, 3) == pytest.approx(0.036)


def test_corrosionrate_conversions():
    cr_mpy = units.UnitConversion.CorrosionRate(1, "mpy")
    cr_mmy = cr_mpy.convert(to_unit="mm_y")

    assert round(cr_mmy, 3) == pytest.approx(0.025)


def test_gasstdrate_conversions():
    qg_mmscfd = units.UnitConversion.GasStandardFlowrate(1, "mmscf_d")
    qg_scfd = qg_mmscfd.convert(to_unit="scf_d")
    qg_mscfd = qg_mmscfd.convert(to_unit="mscf_d")
    qg_sm3d = qg_mmscfd.convert(to_unit="sm3_d")
    qg_sm3s = qg_mmscfd.convert(to_unit="sm3_s")
    qg_msm3d = qg_mmscfd.convert(to_unit="msm3_d")

    assert round(qg_scfd, 1) == pytest.approx(1000000.0)
    assert round(qg_mscfd, 1) == pytest.approx(1000)
    assert round(qg_sm3d, 1) == pytest.approx(28316.8)
    assert round(qg_sm3s, 2) == pytest.approx(0.33)
    assert round(qg_msm3d, 3) == pytest.approx(0.028)

    # qg_mscfd = units.UnitConversion.GasStandardFlowrate(1000, "Mscf_d")
    # qg_mmscfd = qg_mscfd.convert(to_unit="MMscf_d")

    # assert round(qg_mmscfd) == pytest.approx(1)


def test_gor_conversions():
    gor_scfstb = units.UnitConversion.GOR(300, "scf_sbbl")
    gor_mmscfbbl = gor_scfstb.convert(to_unit="mmscf_sbbl")
    gor_sm3sm3 = gor_scfstb.convert(to_unit="sm3_sm3")
    gor_scfscf = gor_scfstb.convert(to_unit="scf_scf")

    assert round(gor_mmscfbbl, 4) == pytest.approx(0.0003)
    assert round(gor_sm3sm3, 1) == pytest.approx(53.4)
    assert round(gor_scfscf, 1) == pytest.approx(53.4)


def test_kinematicvisc_conversions():
    muk_cst = units.UnitConversion.KinematicViscosity(100, "cSt")
    muk_ft2h = muk_cst.convert(to_unit="ft2_h")
    muk_m2s = muk_cst.convert(to_unit="m2_s")
    muk_in2s = muk_cst.convert(to_unit="in2_s")

    assert round(muk_ft2h, 2) == pytest.approx(3.88)
    assert round(muk_m2s, 4) == pytest.approx(0.0001)
    assert round(muk_in2s, 3) == pytest.approx(0.155)


def test_massflowrate_conversions():
    m_kgs = units.UnitConversion.MassFlowrate(1, "kg_s")
    m_lbh = m_kgs.convert(to_unit="lb_h")
    m_td = m_kgs.convert(to_unit="t_d")
    m_lbs = m_kgs.convert(to_unit="lb_s")
    m_gs = m_kgs.convert(to_unit="g_s")
    m_ktd = m_kgs.convert(to_unit="kt_d")

    assert round(m_lbh, 2) == pytest.approx(7936.64)
    assert round(m_td, 1) == pytest.approx(86.4)
    assert round(m_lbs, 1) == pytest.approx(2.2)
    assert round(m_gs, 1) == pytest.approx(1000)
    assert round(m_ktd, 3) == pytest.approx(0.086)


def test_volume_conversions():
    m_bbl = units.UnitConversion.Volume(1000, "bbl")
    m_l = m_bbl.convert(to_unit="L")
    m_m3 = m_bbl.convert(to_unit="m3")
    m_ft3 = m_bbl.convert(to_unit="ft3")
    m_gal = m_bbl.convert(to_unit="gal")
    m_cm3 = m_bbl.convert(to_unit="cm3")
    m_mmft3 = m_bbl.convert(to_unit="mmft3")
    m_ml = m_bbl.convert(to_unit="mL")

    assert round(m_l, 1) == pytest.approx(158987.3)
    assert round(m_m3, 3) == pytest.approx(158.987)
    assert round(m_ft3, 1) == pytest.approx(5614.6)
    assert round(m_gal, 1) == pytest.approx(42000)
    assert round(m_cm3, 1) == pytest.approx(158987294.9)
    assert round(m_mmft3, 4) == pytest.approx(0.0056)
    assert round(m_ml, 1) == pytest.approx(158987294.9)


def test_conductivity_conversions():
    k_wmk = units.UnitConversion.ThermalConductivity(1000, "w_mk")
    k_wmc = k_wmk.convert(to_unit="w_mc")
    k_calmhk = k_wmk.convert(to_unit="cal_mhk")
    k_btufthR = k_wmk.convert(to_unit="btu_fthr")

    assert round(k_wmc, 1) == pytest.approx(1000)
    assert round(k_calmhk, 1) == pytest.approx(860420.65)
    assert round(k_btufthR, 2) == pytest.approx(578.18)


def test_deltatemp_conversions():
    dt_c = units.UnitConversion.TemperatureDifference(12.3, "delta_degC")
    dt_f = dt_c.convert(to_unit="delta_degF")

    assert round(dt_f, 2) == pytest.approx(22.14)


def test_cp_conversions():
    cp_jkgc = units.UnitConversion.SpecificHeatCapacity(100, "j_kgc")
    cp_btulbf = cp_jkgc.convert(to_unit="btu_lbf")
    cp_btulbr = cp_jkgc.convert(to_unit="btu_lbr")
    cp_jkgk = cp_jkgc.convert(to_unit="j_kgk")

    assert round(cp_btulbf, 2) == pytest.approx(0.02)
    assert round(cp_btulbr, 2) == pytest.approx(0.02)
    assert round(cp_jkgk, 1) == pytest.approx(100)


def test_energy_conversions():
    en_btu = units.UnitConversion.Energy(1, "btu")
    en_cal = en_btu.convert(to_unit="cal")
    en_j = en_btu.convert(to_unit="j")

    assert round(en_cal, 2) == pytest.approx(252.21)
    assert round(en_j, 1) == pytest.approx(1054.6)


def test_surfacetension_conversions():
    st_nm = units.UnitConversion.SurfaceTension(1, "n_m")
    st_dyncm = st_nm.convert(to_unit="dyn_cm")
    st_mnm = st_nm.convert(to_unit="mn_m")

    assert round(st_dyncm, 1) == pytest.approx(1000.0)
    assert round(st_mnm, 1) == pytest.approx(1000.0)


def test_molecularweight_conversions():
    mw_gmol = units.UnitConversion.MolecularWeight(44.01, "g_mol")
    mw_kgmol = mw_gmol.convert(to_unit="kg_mol")
    mw_kgkmol = mw_gmol.convert(to_unit="kg_kmol")
    mw_lblbmol = mw_gmol.convert(to_unit="lb_lbmol")

    assert round(mw_kgmol, 3) == pytest.approx(0.044)
    assert round(mw_kgkmol, 2) == pytest.approx(44.01)
    assert round(mw_lblbmol, 2) == pytest.approx(44.01)


def test_molarvol_conversions():
    mv_m3mol = units.UnitConversion.MolarVolume(1, "m3_mol")
    mv_cm3mol = mv_m3mol.convert(to_unit="cm3_mol")
    mv_lmol = mv_m3mol.convert(to_unit="l_mol")
    mv_ft3lbmol = mv_m3mol.convert(to_unit="ft3_lbmol")

    assert round(mv_cm3mol, 1) == pytest.approx(1000000)
    assert round(mv_lmol, 1) == pytest.approx(1000)
    assert round(mv_ft3lbmol, 2) == pytest.approx(16018.46)
