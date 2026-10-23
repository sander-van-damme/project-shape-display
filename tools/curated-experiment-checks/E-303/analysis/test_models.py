"""Independent analytical identities and failure-mode checks; stdlib unittest."""
import itertools
import math
import unittest
from model import *


class ScrewAndUnits(unittest.TestCase):
    def test_torque_units(self):
        # One newton at one millimetre is 0.001 Nm = 1 Nmm = 1 mNm.
        self.assertAlmostEqual(friction_torque(1, 1, .001), .001)
        self.assertAlmostEqual(G0 * .001 * .020 * 1000, .196133)

    def test_ideal_energy_per_turn(self):
        torque = efficiency_torque(2, .003, 1)
        self.assertAlmostEqual(torque * 2 * pi, 2 * .003)

    def test_efficiency_and_load_scaling(self):
        t = efficiency_torque(.2, .003, .5)
        self.assertAlmostEqual(efficiency_torque(.4, .003, .25), 4*t)

    def test_frictionless_thread(self):
        t = thread_torque(1, .003, .0023, 0)
        self.assertAlmostEqual(t, efficiency_torque(1, .003, 1))
        self.assertAlmostEqual(thread_torque(1,.003,.0023,0,direction="lower"), -t)

    def test_thread_self_lock_threshold(self):
        crit = .003/(pi*.0023)*cos(pi/4)
        self.assertAlmostEqual(thread_torque(1,.003,.0023,crit,direction="lower"),0)
        self.assertLess(thread_torque(1,.003,.0023,crit*.9,direction="lower"),0)
        self.assertGreater(thread_torque(1,.003,.0023,crit*1.1,direction="lower"),0)

    def test_screw_linear_dimension_covariance(self):
        self.assertAlmostEqual(thread_torque(1,.006,.0046,.2),
                               2*thread_torque(1,.003,.0023,.2))

    def test_starting_friction_increases_required_torque(self):
        self.assertGreater(screw_scenario(.2,.05,.3,2e-5)[0],
                           screw_scenario(.2,.05,.2,2e-5)[0])

    def test_guide_can_require_drive_down(self):
        _, t = screw_scenario(.01,.1,.1,0,mu_thrust=0)
        self.assertGreater(t,0)
        self.assertAlmostEqual(t,thread_torque(.09,.003,.0023,.1))

    def test_invalid_efficiency(self):
        for eta in [0,-1,1.1]:
            with self.assertRaises(ValueError):
                efficiency_torque(1,.003,eta)


class FrictionAndMagnetics(unittest.TestCase):
    def test_disc_effective_radius(self):
        a,rp,rw=annulus(.003)
        self.assertAlmostEqual(a,pi*9e-6)
        self.assertAlmostEqual(rp,.002)
        self.assertAlmostEqual(rw,.0015)

    def test_annulus_quadrature(self):
        # Numerical integrate torque from independent concentric pressure strips.
        ri,ro=.0011,.00235
        n=10000; dr=(ro-ri)/n
        numerical=sum(2*pi*(ri+(k+.5)*dr)**2*dr for k in range(n))
        a,rp,_=annulus(ro,ri)
        self.assertAlmostEqual(numerical/(a*rp),1,places=8)

    def test_wear_radius_thin_ring(self):
        _,rp,rw=annulus(.002,.001999)
        self.assertAlmostEqual(rp,rw,places=9)

    def test_force_torque_and_surface_count(self):
        self.assertAlmostEqual(friction_torque(.2,.3,.002,2),.00024)

    def test_single_gap_maxwell_pressure(self):
        # Negligible reluctance in arbitrarily permeable steel branch.
        m=magnetic_circuit(20,[(.0001,1e-6)],[(.001,1e-6,1e12)])
        b=MU0*20/.0001
        self.assertAlmostEqual(m['linear_force_n'],b*b*1e-6/(2*MU0),places=10)

    def test_two_gaps_are_series_not_parallel(self):
        one=magnetic_circuit(10,[(.0001,1e-6)],[(.001,1e-6,1e12)])
        two=magnetic_circuit(10,[(.0001,1e-6)]*2,[(.001,1e-6,1e12)])
        self.assertAlmostEqual(two['flux_wb']/one['flux_wb'],.5,places=8)
        # Twice the area at half B gives half TOTAL force, not twice the force.
        self.assertAlmostEqual(two['linear_force_n']/one['linear_force_n'],.5,places=8)

    def test_unsaturated_force_is_current_squared(self):
        args=([(.0001,1e-6)]*2,[(.01,1e-6,300)])
        a=magnetic_circuit(10,*args); b=magnetic_circuit(20,*args)
        self.assertAlmostEqual(b['linear_force_n'],4*a['linear_force_n'])

    def test_small_bridge_flags_invalid_linear_prediction(self):
        m=magnetic_circuit(100,[(.00002,2e-6)]*2,[(.01,2e-6,1000)],
                           bottleneck_m2=.1e-6)
        self.assertFalse(m['below_core_limit'])
        self.assertLess(m['screen_force_n'],m['linear_force_n'])

    def test_fixed_gap_does_not_add_armature_force(self):
        a=magnetic_circuit(10,[(.0001,1e-6)]*2,[(.01,1e-6,300)])
        b=magnetic_circuit(10,[(.0001,1e-6)]*2,
                           [(.01,1e-6,300),(.00005,1e-6,1)])
        self.assertLess(b['linear_force_n'],a['linear_force_n'])

    def test_winding_power_energy(self):
        c=winding(.0024,.0046,.003)
        o=coil_operating_point(c,30,.2)
        self.assertAlmostEqual(o['power_w'],o['voltage_v']*o['current_a'])
        self.assertAlmostEqual(o['average_power_w'],.2*o['power_w'])
        self.assertAlmostEqual(o['initial_adiabatic_k_per_s']*c['copper_mass_kg']*385,o['power_w'])


class ElectrostaticsAndPower(unittest.TestCase):
    def setUp(self):
        self.args=(10e-6,.002,300,12e-6,3.25)

    def test_gap_force_virtual_work(self):
        # Independent finite difference of capacitance at fixed voltage.
        a,r,v,t,er=self.args; g=5e-6; h=1e-10
        cap=lambda gg:EPS0*a/(gg+t/er)
        force=-.5*v*v*(cap(g+h)-cap(g-h))/(2*h)
        self.assertAlmostEqual(force,electrostatic(*self.args,gap_m=g)['normal_gap_n'],places=9)

    def test_bulk_pressure_virtual_work(self):
        a,r,v,t,er=self.args; h=1e-10
        cap=lambda tt:EPS0*er*a/tt
        pressure=-.5*v*v*(cap(t+h)-cap(t-h))/(2*h)/a
        self.assertAlmostEqual(pressure/electrostatic(*self.args)['bulk_pressure_pa'],1,places=8)

    def test_floating_equal_split_quarter(self):
        a=electrostatic(*self.args); b=electrostatic(*self.args,split=True)
        for key in ['capacitance_f','torque_gap_nm','stored_energy_j']:
            self.assertAlmostEqual(b[key]/a[key],.25)

    def test_series_capacitance_derivation(self):
        full=electrostatic(*self.args)['capacitance_f']
        half=full/2
        series=1/(1/half+1/half)
        self.assertAlmostEqual(series,electrostatic(*self.args,split=True)['capacitance_f'])

    def test_unequal_floating_charge_and_stray(self):
        self.assertAlmostEqual(floating_voltage(1e-12,2e-12,300,0),100)
        self.assertAlmostEqual(floating_voltage(1e-12,1e-12,300,0,stray_c_f=1e-12),100)
        self.assertAlmostEqual(floating_voltage(1e-12,1e-12,300,0,net_charge_c=1e-10),200)

    def test_voltage_square_and_field(self):
        a=electrostatic(*self.args)
        b=electrostatic(10e-6,.002,600,12e-6,3.25)
        self.assertAlmostEqual(b['torque_gap_nm'],4*a['torque_gap_nm'])
        self.assertAlmostEqual(a['dielectric_field_v_per_m'],25e6)

    def test_airgap_loss(self):
        a=electrostatic(*self.args)
        b=electrostatic(*self.args,gap_m=12e-6/3.25)
        self.assertAlmostEqual(b['torque_gap_nm'],a['torque_gap_nm']/4)

    def test_cubic_scaling_only_when_radial_geometry_scales(self):
        a,r,_=annulus(.01,.002)
        large=electrostatic(a,r,300,12e-6,3.25)
        a,r,_=annulus(.0025,.0005)
        small=electrostatic(a,r,300,12e-6,3.25)
        self.assertAlmostEqual(small['torque_gap_nm']/large['torque_gap_nm'],.25**3)
        a,r,_=annulus(.0025,.002) # Fixed hub violates geometric similarity.
        fixedhub=electrostatic(a,r,300,12e-6,3.25)
        self.assertNotAlmostEqual(fixedhub['torque_gap_nm']/large['torque_gap_nm'],.25**3)

    def test_cycle_energy_not_half_energy(self):
        e=electrostatic(*self.args)
        self.assertAlmostEqual(e['resistive_cycle_energy_j'],2*e['stored_energy_j'])

    def test_discharge_force_decay(self):
        v=retained_voltage(300,.001,1e8,10e-12)
        self.assertAlmostEqual((v/300)**2,math.exp(-2))

    def test_slip_power_and_array_scale(self):
        self.assertAlmostEqual(slip_heat(.0001,600),.006283185307)
        self.assertEqual(electrical_power(6400,.01),64)


class GeometryAndAddressing(unittest.TestCase):
    def test_lattice_diagonal_neighbor(self):
        self.assertAlmostEqual(nearest_same_tier(.00508,2),sqrt(2)*.00508)
        self.assertAlmostEqual(nearest_same_tier(.00508,4),2*.00508)

    def test_stagger_does_not_remove_shaft_collision(self):
        self.assertGreater(nearest_same_tier(.00508,4)-.010,0)
        self.assertLess(.00508-.010/2-.0032/2,0)

    def test_bipolar_unsigned_diagonal_is_possible(self):
        self.assertEqual(matrix_voltages([0,1],[1,0]),((-1,0),(0,1)))
        self.assertEqual(matrix_on([0,1],[1,0]),((True,False),(False,True)))

    def test_diode_cannot_select_both_diagonal(self):
        diag=((True,False),(False,True))
        patterns={matrix_on(b[:2],b[2:],"diode") for b in itertools.product([0,1],repeat=4)}
        self.assertEqual(len(patterns),10)
        self.assertNotIn(diag,patterns)

    def test_unsigned_two_rail_masks_not_arbitrary(self):
        patterns={matrix_on(b[:2],b[2:]) for b in itertools.product([0,1],repeat=4)}
        self.assertEqual(len(patterns),8)
        self.assertNotIn(((True,True),(True,False)),patterns)

    def test_analog_three_corners_needs_unequal_forces(self):
        vals=matrix_voltages([0,1],[-1,0])
        self.assertEqual(vals,((1,0),(2,1)))
        self.assertEqual([[v*v for v in row] for row in vals],[[1,0],[4,1]])

    def test_signed_voltage_rectangle_identity(self):
        for r1,r2,c1,c2 in itertools.product(range(-2,3),repeat=4):
            v=matrix_voltages([r1,r2],[c1,c2])
            self.assertEqual(v[0][0]+v[1][1],v[0][1]+v[1][0])

    def test_analog_3x3_identity_fails_finite_voltage_search(self):
        # Companion to analytic middle-column proof in calculations.md. This finite
        # search is a representative test, not a proof for arbitrary voltages.
        identity=tuple(tuple(i==j for j in range(3)) for i in range(3))
        for b in itertools.product(range(-2,3),repeat=6):
            state=tuple(tuple(abs(r-c)>=1 for c in b[3:]) for r in b[:3])
            self.assertNotEqual(state,identity)


if __name__ == '__main__':
    unittest.main(verbosity=2)
