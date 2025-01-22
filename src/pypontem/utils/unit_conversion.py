import pint
import math

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

unit_map = {
    "S": "second",
    "Min": "minute",
    "H": "hour",
    "D": "day",
    "W": "week",
    "M": "month",
    "Y": "year",
}


class UnitConversion:
    class Acceleration:
        """Creates an acceleration object that can store an acceleration value and
        convert between units of acceleration."""

        ureg.define("m_s2 = meter / (second ** 2)")
        ureg.define("ft_s2 = 381/1250 * m_s2")
        ureg.define("in_s2 = 127/5000 * m_s2")
        ureg.define("cm_s2 = 1/100 * m_s2")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the acceleration to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Angle:
        """Creates an angle object that can store an angle value and
        convert between units of angle."""

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the angle to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class AngularVelocity:

        ureg.define("deg_s = degree / second")
        ureg.define("rad_s = 10800 / 3.1415926535897932384626433 * deg_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class Area:
        """Creates an area object that can store an area value and
        convert between units of area."""

        ureg.define("ft2 = 1 * sq_ft")
        ureg.define("m2 = 1562500/145161 * ft2")
        ureg.define("cm2 = 625/580644 * ft2")
        ureg.define("in2 = 1/144 * ft2")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the area to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class AreaPerLength:
        """Creates an object representing area per length and allows for unit conversions."""

        ureg.define("m2_m = (meter ** 2) / meter")
        ureg.define("in2_ft = 127/60000 * m2_m")
        ureg.define("mm2_m = 1/1000000 * m2_m")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the area per length to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Unitless:
        """Creates an object representing a unitless quantity."""

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Returns the value unchanged, as it is a unitless quantity."""
            return self.value

    class BrineDensity:
        """Creates an object representing brine density and allows for unit conversions.
        - g/cm3: Grams per cubic centimeter
        - kg/m3: Kilograms per cubic meter
        - lb/ft3: lb per cubic foot
        - lb/in3: lb per cubic inch
        - ppg: lb per gallon
        - mg/L: Milligrams per liter
        """

        ureg.define("g_cm3 = gram / (centimeter ** 3)")
        ureg.define("kg_m3 = 1 / 1000 * g_cm3")
        ureg.define("lb_ft3 = 226796185 / 14158423296 * g_cm3")
        ureg.define("lb_in3 = 226796185 / 8193532 * g_cm3")
        ureg.define("ppg = 2945405 / 24580596 * g_cm3")
        ureg.define("mg_l = 1 / 1000000 * g_cm3")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the brine density to the specified unit."""

            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class CGR:
        """Creates and allows CGR unit conversions.
        - CGR: Condensate Gas Ratio
        - scf/scf: Standard cubic feet per standard cubic feet
        - sm3/sm3: Standard cubic meters per standard cubic meter
        - sm3/MMsm3: Standard cubic meters per million standard cubic meters
        - sbbl/MMscf: Stock tank barrels per million standard cubic feet
        - sbbl/scf: Stock tank barrels per standard cubic feet
        """

        ureg.define("scf_scf = ((foot ** 3) / (foot ** 3))")
        ureg.define("sm3_sm3 = 1 * scf_scf")
        ureg.define("sm3_mmsm3 = 1 / 1000000 * scf_scf")
        ureg.define("sbbl_mmscf = 539 / 96000000 * scf_scf")
        ureg.define("sbbl_scf = 539 / 96 * scf_scf")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the CGR to the specified unit."""

            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class CorrosionRate:
        """
        convert between units of corrosion rate.
        - m/s: Meters per second
        - m/yr: Meters per year
        - mm/yr: Millimeters per year
        - mpy: Mil per year (Mil is a unit of length equal to one thousandth of an inch)
        """

        ureg.define("m_s = meter / second")
        ureg.define("m_y = 1 / 31536000 * m_s")
        ureg.define("mm_y = 1 / 31536000000 * m_s")
        ureg.define("mpy = 127 / 157680000000000 * m_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the corrosion rate to the specified unit."""

            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Density:
        """Creates density and allows for unit conversions.
        - g/cm3: Grams per cubic centimeter
        - kg/m3: Kilograms per cubic meter
        - lb/ft3: lb per cubic foot
        - lb/in3: lb per cubic inch
        """

        ureg.define("g_cm3 = 1 * (gram / centimeter ** 3)")
        ureg.define("kg_m3 = 1 / 1000 * g_cm3")
        ureg.define("lb_ft3 = 226796185 / 14158423296 * g_cm3")
        ureg.define("lb_in3 = 226796185 / 8193532 * g_cm3")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the density to the specified unit."""

            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class DensityPerPressure:
        """allows density per pressure unit conversions
        - kg/m-N: Kilograms per meter per Newton
        - s2/m2: Seconds squared per square meter
        """

        ureg.define("kg_mn = kilogram / (meter * newton)")
        ureg.define("s2_m2 = second ** 2 / meter ** 2")
        ureg.define("kg_mn = 1 * s2_m2")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the density to the specified unit."""

            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class DensityPerTemperature:
        """allows density per temperature unit conversions
        - kg/m3-C: Kilograms per cubic meter per degree Celsius
        - kg/m3-K: Kilograms per cubic meter per Kelvin
        """

        ureg.define("kg_m3k = kilogram / ((meter ** 3) * kelvin)")
        ureg.define("kg_m3c = 1 * kg_m3k")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the density to the specified unit."""

            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class DiffusionCoefficient:
        """allows DiffusionCoefficient unit conversions
        - cm2/s: square centimeters per second
        - m2/s: square meters per second
        - mm2/s: square millimeters per second
        """

        ureg.define("cm2_s = (centimeter ** 2) / second")
        ureg.define("m2_s = 10000 * cm2_s")
        ureg.define("mm2_s = 1 / 100 * cm2_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the density to the specified unit."""

            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Distance:
        """Creates an angle object that can store an angle value and
        convert between units of angle."""

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the angle to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class DynamicViscosity:
        """Allows Dynamic Viscosity unit conversions.
        - cp: Centipoise
        - kg/m-h: Kilograms per meter per hour
        - kg/m-s: Kilograms per meter per second
        - mPa-s: Millipascal-seconds
        - N-s/m²: Newton-seconds per square meter
        - Pa-s: Pascal-seconds
        - lb/ft-h: lb per foot per hour
        """

        ureg.define("cp = 1 * centipoise")
        ureg.define("pas = 1000 * cp")
        ureg.define("kg_mh = 5/18 * cp")
        ureg.define("kg_ms = 1000 * cp")
        ureg.define("ns_m2 = 1000 * cp")
        ureg.define("mpas = 1 * cp")
        ureg.define("lb_fth = 45359237/109728000 * cp")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the area to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Energy:
        """
        Allows for energy unit conversion:
        - BTU: British Thermal Unit
        - CAL: Calorie
        - J: Joule
        """

        ureg.define("btu = 1 * Btu")
        ureg.define("cal = 0.003965 * btu")
        ureg.define("j = 0.00094823 * btu")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the angle to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Enthalpy:
        """
        Allows for Enthalpy unit conversion:
        - BTU: British Thermal Unit
        - CAL: Calorie
        - J: Joule
        """

        ureg.define("btu = 1 * Btu")
        ureg.define("cal = 0.003965 * btu")
        ureg.define("j = 0.00094823 * btu")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the angle to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class EnthalpyPerMass:
        """
        Allows for EnthalpyPerMass unit conversion:
        British Thermal Units per Pound (btu/lb)
        Joules per Kilogram (J/kg)
        Kilojoules per Kilogram (kJ/kg)
        """

        ureg.define("btu_lb = 1 * (Btu /pound) ")
        ureg.define("j_kg = 4123567 / 9585002404 * btu_lb")
        ureg.define("kj_kg = 1030891750 / 2396250601 * btu_lb")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the angle to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class EnthalpyPerMol:
        """
        Allows for Enthalpy Per Mol unit conversion:
        British Thermal Units per Pound-mole (btu/lbmol)
        Calories per Mole (cal/mol)
        Joules per Mole (J/mol)
        """

        ureg.define("j_mol = joule / mole")
        ureg.define("cal_mol = 523/125 * j_mol")
        ureg.define("btu_lbmol = 2396250601/1030891750 * j_mol")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the enthalpy per mol to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class EnthalpyPerMolPerTemperature:
        """
        Allows for Enthalpy Per Mol Per Temperature unit conversion:
        British Thermal Units per Pound-mole per Rankine (btu/lbmol-R)
        Joules per Mole per Kelvin (J/mol-K)
        """

        ureg.define("btu_lbmolr = 1 * (Btu / (pound * mole * rankine))")
        ureg.define("j_molk = 5154458750 / 21566255409 * btu_lbmolr")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the enthalpy per mol per temperature to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class EnthalpyPerVolume:
        """
        Allows for Enthalpy Per Volume unit conversion:
        British Thermal Units per Cubic Foot (btu/ft^3)
        Calories per Cubic Meter (cal/m^3)
        Joules per Cubic Meter (J/m^3)
        """

        ureg.define("btu_ft3 = 1* (Btu / (foot ** 3))")
        ureg.define("cal_m3 = 231401730744 / 2059277860234375 * btu_ft3")
        ureg.define("j_m3 = 442450728 / 16474222881875 * btu_ft3")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the enthalpy per volume to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Entropy:
        """
        Allows for Entropy unit conversion:
        British Thermal Units per Rankine (btu/R)
        Calories per Kelvin (cal/K)
        Joules per Kelvin (J/K)
        """

        ureg.define("btu_r = 1 * (Btu / rankine)")
        ureg.define("cal_K = 523000000 / 237228809499 * btu_r")
        ureg.define("j_K = 125000000 / 237228809499 * btu_r")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the entropy to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class EntropyPerMass:
        """
        Allows for Entropy Per Mass unit conversion:
        British Thermal Units per Pound per Fahrenheit (btu/lb-F)
        Joules per Kilogram per Celsius (J/kg-C)
        Kilojoules per Kilogram per Celsius (kJ/kg-C)
        """

        ureg.define("j_kgc = 1 * (joule / (kilogram * degC))")
        ureg.define("btu_lbf = 86265021636/20617835 * j_kgc")
        ureg.define("kj_kgc = 1000 * j_kgc")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the entropy per mass to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class EntropyPerMol:
        """
        Allows for Entropy Per Mol unit conversion:
        British Thermal Units per Pound per Rankine (btu/lbmol-R)
        Calories per Mol per Kelvin (cal/mol-K)
        Joules per Mol per Kelvin (J/mol-K)
        """

        ureg.define("j_molk = 1 * (joule / (mole * degK))")
        ureg.define("cal_molk = 523/125 * j_molk")
        ureg.define("btu_lbmolr = 21566255409/5154458750 * j_molk")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the entropy per mol to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class EntropyPerVolume:
        """
        Allows for Entropy Per Volume unit conversion:
        British Thermal Units per Cubic Foot per Rankine (btu/ft^3-R)
        Calories per Cubic Meter per Kelvin (cal/m^3-K)
        Joules per Cubic Meter per Kelvin (J/m^3-K)
        """

        ureg.define("j_m3k = joule / ((meter ** 3) * degK)")
        ureg.define("cal_m3k = 523/125 * j_m3k")
        ureg.define("btu_ft3r = 411855572046875/25711303416 * j_m3k")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the entropy per volume to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class ErosionRate:
        """
        Allows for Erosion Rate unit conversion:
        Inches per Year (in/yr)
        Millimeters per Year (mm/yr)
        Inches per Thousand Years (in/kyr)
        """

        ureg.define("in_y = 1 * (inch / year)")
        ureg.define("mm_y = 5 / 127 * in_y")
        ureg.define("in_kyr = 1 / 1000 * in_y")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the erosion rate to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Force:
        """
        Allows for Force unit conversion:
        Dyne (dyn)
        Kilogram-force (kgf)
        Newton (N)
        Pound-force (lbf)
        """

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the angle to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Fraction:
        """
        Allows Fraction unit conversions:
        Parts per billion (ppb)
        Parts per million (ppm)
        Percent (%)
        Dimensionless (-)
        """

        ureg.define("ppm = 1 * ppm")
        ureg.define("ppb = 1 / 1000 * ppm")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert_to(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Frequency:
        """
        Allows Frequency unit conversions:
        Hertz (Hz)
        Inverse hour (1/h)
        Inverse minute (1/min)
        Inverse second (1/s)
        """

        ureg.define("hz = 1 * hertz")
        ureg.define("one_h = 1 / 3600 * hz")
        ureg.define("one_m = 1 / 60 * hz")
        ureg.define("one_s = 1 * hz")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class FrictionFactor:
        """
        Allows Friction Factor unit conversions:
        Newton-second per meter (N-s/m)
        """

        ureg.define("ns_m = (newton * second) / meter")
        ureg.define("g_s = 1 / 1000 * ns_m")
        ureg.define("kg_h = 1 / 3600 * ns_m")
        ureg.define("kg_s = 1 * ns_m")
        ureg.define("kt_d = 625 / 54 * ns_m")
        ureg.define("lb_h = 45359237 / 360000000000 * ns_m")
        ureg.define("lb_s = 45359237 / 100000000 * ns_m")
        ureg.define("t_d = 5 / 432 * ns_m")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class GasFlowrate:
        """
        Allows Gas Flowrate unit conversions:
        Barrel per day (bbl/d)
        Barrel per hour (bbl/h)
        Barrel per minute (bbl/min)
        Cubic foot per day (ft3/d)
        Cubic foot per hour (ft3/h)
        Cubic foot per minute (ft3/min)
        Cubic foot per second (ft3/s)
        Cubic meter per day (m3/d)
        Cubic meter per hour (m3/h)
        Cubic meter per second (m3/s)
        Gallon per minute (gpm)
        Liter per minute (L/min)
        Milliliter per minute (mL/min)
        """

        ureg.define("m3_s = (meter ** 3) / second")
        ureg.define("bbl_d = 1104078437 / 600000000000000 * m3_s")
        ureg.define("bbl_h = 1104078437 / 25000000000000 * m3_s")
        ureg.define("bbl_min = 3312235311 / 1250000000000 * m3_s")
        ureg.define("ft3_d = 2048383 / 6250000000000 * m3_s")
        ureg.define("ft3_h = 6145149 / 781250000000 * m3_s")
        ureg.define("ft3_min = 18435447 / 39062500000 * m3_s")
        ureg.define("ft3_s = 55306341 / 1953125000 * m3_s")
        ureg.define("m3_d = 1 / 86400 * m3_s")
        ureg.define("m3_h = 1 / 3600 * m3_s")
        ureg.define("gpm = 157725491 / 2500000000000 * m3_s")
        ureg.define("l_min = 1 / 60000 * m3_s")
        ureg.define("ml_min = 1 / 60000000 * m3_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class GasStandardFlowrate:
        """
        Allows Gas Standard Flowrate unit conversions:
        Million standard cubic feet per day (MMscf/d)
        Standard cubic feet per day (scf/d)
        Standard cubic feet per hour (scf/h)
        Standard cubic feet per second (scf/s)
        Standard cubic meter per day (sm3/d)
        Standard cubic meter per hour (sm3/h)
        Standard cubic meter per second (sm3/s)
        Thousand standard cubic feet per day (Mscf/d)
        Thousand standard cubic meters per day (Msm3/d)
        Thousand standard cubic meters per hour (Msm3/h)
        """

        ureg.define("sm3_s = (meter ** 3) / second")
        ureg.define("mmscf_d = 2048383/6250000 * sm3_s")
        ureg.define("scf_d = 2048383/6250000000000 * sm3_s")
        ureg.define("scf_h = 6145149/781250000000 * sm3_s")
        ureg.define("scf_s = 55306341/1953125000 * sm3_s")
        ureg.define("sm3_d = 1/86400 * sm3_s")
        ureg.define("sm3_h = 1/3600 * sm3_s")
        ureg.define("mscf_d = 2048383/6250000000 * sm3_s")
        ureg.define("msm3_d = 625/54 * sm3_s")
        ureg.define("msm3_h = 2500/9 * sm3_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class GLR:
        """
        Allows Gas-Liquid Ratio unit conversions:
        MMscf/sbbl (Million standard cubic feet per stock barrel)
        scf/scf (Standard cubic feet per standard cubic feet)
        scf/sbbl (Standard cubic feet per stock barrel)
        sm3/sm3 (Standard cubic meter per standard cubic meter)
        """

        ureg.define("sm3_sm3 = ((meter ** 3) / (meter ** 3))")
        ureg.define("mmscf_sbbl = 96000000 / 539 * sm3_sm3")
        ureg.define("scf_scf = 1 * sm3_sm3")
        ureg.define("scf_sbbl = 96 / 539 * sm3_sm3")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class GOR:
        """
        Allows Gas-Oil Ratio unit conversions:
        MMscf/sbbl (Million standard cubic feet per stock barrel)
        scf/scf (Standard cubic feet per standard cubic feet)
        scf/sbbl (Standard cubic feet per stock barrel)
        sm3/sm3 (Standard cubic meter per standard cubic meter)
        """

        ureg.define("sm3_sm3 = ((meter ** 3) / (meter ** 3))")
        ureg.define("mmscf_sbbl = 96000000 / 539 * sm3_sm3")
        ureg.define("scf_scf = 1 * sm3_sm3")
        ureg.define("scf_sbbl = 96 / 539 * sm3_sm3")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class HeatFlux:
        """
        Allows Heat Flux unit conversions:
        btu/ft2-s (British thermal unit per square foot per second)
        btu/in2 (British thermal unit per square inch per second)
        kW/m2 (Kilowatt per square meter)
        W/cm2 (Watt per square centimeter)
        W/m2 (Watt per square meter)
        """

        ureg.define("w_m2 = watt / (meter ** 2)")
        ureg.define("btu_ft2s = 26358756611/2322576 * w_m2")
        ureg.define("btu_in2s = 26358756611/16129 * w_m2")
        ureg.define("kw_m2 = 1000 * w_m2")
        ureg.define("w_cm2 = 10000 * w_m2")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class HeatTransferCoefficient:
        """
        Allows Heat Transfer Coefficient unit conversions:
        btu/ft2-h-F (British thermal unit per square foot per hour per Fahrenheit degree)
        cal/m2-h-C (Calorie per square meter per hour per Celsius degree)
        W/m2-C (Watt per square meter per Celsius degree)
        W/m2-K (Watt per square meter per Kelvin degree)
        """

        ureg.define("w_m2c = watt / (meter ** 2) * degC")
        ureg.define("W_m2k = 1 * w_m2c")
        ureg.define("btu_ft2hf = 26358756611/4645152000 * w_m2c")
        ureg.define("cal_m2hc = 523/450000 * w_m2c")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class HeatTransferPerLength:
        """
        Allows Heat Transfer Per Length unit conversions:
        British Thermal Unit per second per foot (btu/s-ft)
        Kilowatt per meter (kW/m)
        Watt per meter (W/m)
        """

        ureg.define("w_m = 1 * (watt / meter)")
        ureg.define("btu_sft = 26358756611 / 7620000 * w_m")
        ureg.define("kw_m = 1000 * w_m")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class KinematicViscosity:
        """
        Allows Kinematic Viscosity unit conversions:
        Centistokes (cSt)
        Square foot per hour (ft2/h)
        Square inch per second (in2)
        Square meter per second (m2/s)
        """

        ureg.define("m2_s = (meter ** 2) / second")
        ureg.define("cst =  1 / 1000000 * m2_s")
        ureg.define("ft2_h = 16129 / 625000000 *m2_s")
        ureg.define("in2_s = 16129 / 25000000 * m2_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Length:
        """
        Allows Length unit conversions:
        Centimeter (cm)
        Foot (ft)
        Inch (in)
        Kilometer (km)
        Meter (m)
        Micrometer (µm)
        Mile (mi)
        Millimeter (mm)
        Yard (yd)
        """

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class LinearMomentum:
        """
        Allows Linear Momentum unit conversions:
        Kilogram-meter per second (kg-m/s)
        Newton-second (N-s)
        """

        ureg.define("ns = 1 * (newton * second)")
        ureg.define("kgm_s = 1 * ns")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class LiquidFlowRate:
        """
        Allows Liquid Flowrate unit conversions:
        Barrels per day (bbl/d)
        Barrels per hour (bbl/h)
        Barrels per minute (bbl/min)
        Cubic feet per day (ft3/d)
        Cubic feet per hour (ft3/h)
        Cubic feet per minute (ft3/min)
        Cubic feet per second (ft3/s)
        Cubic meters per day (m3/d)
        Cubic meters per hour (m3/h)
        Cubic meters per second (m3/s)
        Gallons per minute (gpm)
        Liters per minute (L/min)
        Milliliters per minute (mL/min)
        """

        ureg.define("m3_s = (meter ** 3) / second")
        ureg.define("bbl_d = 1104078437 / 600000000000000 * m3_s")
        ureg.define("bbl_h = 1104078437 / 25000000000000 * m3_s")
        ureg.define("bbl_min = 3312235311 / 1250000000000 * m3_s")
        ureg.define("ft3_d = 2048383 / 6250000000000 * m3_s")
        ureg.define("ft3_h = 6145149 / 781250000000 * m3_s")
        ureg.define("ft3_min = 18435447 / 39062500000 * m3_s")
        ureg.define("ft3_s = 55306341 / 1953125000 * m3_s")
        ureg.define("m3_d = 1 / 86400 * m3_s")
        ureg.define("m3_h = 1 / 3600 * m3_s")
        ureg.define("gpm = 157725491 / 2500000000000 * m3_s")
        ureg.define("l_min = 1 / 60000 * m3_s")
        ureg.define("ml_min = 1 / 60000000 * m3_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class LiquidStandardFlowRate:
        """
        Allows Liquid Standard Flowrate unit conversions:
        Standard cubic meters per day (sm3/d)
        Standard cubic meters per hour (sm3/h)
        Standard cubic meters per second (sm3/s)
        Standard barrels per day (sbbl/d)
        Standard barrels per hour (sbbl/h)
        Standard barrels per minute (sbbl/min)
        """

        ureg.define("sm3_s = (meter ** 3) / second")
        ureg.define("sm3_d = 1 / 86400 * sm3_s")
        ureg.define("sm3_h = 1 / 3600 * sm3_s")
        ureg.define("sbbl_d = 1104078437 / 600000000000000* sm3_s")
        ureg.define("sbbl_h = 1104078437 / 25000000000000 * sm3_s")
        ureg.define("sbbl_min = 3312235311 / 1250000000000 * sm3_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Mass:
        """
        Allows Mass unit conversions:
        Gram (g)
        Kilogram (kg)
        Milligram (mg)
        Kiloton (kt)
        Kip (kips)
        Ounce (oz)
        Pound (lb)
        Ton (t)
        """

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the angle to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class MassFlowrate:
        """
        Allows Mass Flowrate unit conversions:
        Gram per second (g/s)
        Kilogram per hour (kg/h)
        Kilogram per second (kg/s)
        Kiloton per day (kt/d)
        Pound per hour (lb/h)
        Pound per second (lb/s)
        Ton per day (t/d)
        """

        ureg.define("g_s = gram / second")
        ureg.define("kg_h = 5/18 * g_s")
        ureg.define("kg_s = 1000 * g_s")
        ureg.define("kt_d = 312500/27 * g_s")
        ureg.define("lb_h = 45359237/360000000 * g_s")
        ureg.define("lb_s = 45359237/100000 * g_s")
        ureg.define("t_d =  625/54 * g_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the mass flowrate to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class MassFlowratePerArea:
        """
        Allows Mass Flowrate Per Area unit conversions:
        Kilogram per hour per square meter (kg/h-m2)
        Kilogram per hour per square centimeter (kg/h-cm2)
        Kilogram per second per square meter (kg/s-m2)
        Pound per hour per square meter (lb/h-m2)
        Pound per second per square meter (lb/s-m2)
        Milligram per hour per square inch (mg/h-in2"""

        ureg.define("kg_hm2 = 1 * (kilogram / hour * (meter ** 2))")
        ureg.define("kg_hcm2 = 10000 * kg_hm2")
        ureg.define("kg_sm2 = 3600 * kg_hm2 ")
        ureg.define("lb_hm2 = 45359237 / 100000000 * kg_hm2")
        ureg.define("lb_sm2 = 408233133 / 250000 * kg_hm2")
        ureg.define("mg_hin2 = 25 / 16129 * kg_hm2")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the mass flowrate per area to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class MassGradient:
        """
        Allows Mass Gradient unit conversions:
        Gram per centimeter (g/cm)
        Gram per foot (g/ft)
        Gram per inch (g/in)
        Gram per meter (g/m)
        Kilogram per meter (kg/m)
        Pound per foot (lb/ft)
        Pound per inch (lb/in)
        """

        ureg.define("g_m = 1 * (gram / meter)")
        ureg.define("g_cm = 100 * g_m")
        ureg.define("g_ft = 1250 / 381 * g_m")
        ureg.define("g_in = 5000 / 127 * g_m")
        ureg.define("kg_m = 1000 * g_m")
        ureg.define("lb_ft = 45359237 / 30480 * g_m")
        ureg.define("lb_in = 45359237 / 2540 * g_m")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class MassMomentOfInertia:
        """
        Allows Mass Moment of Inertia unit conversions:
        Kilogram square meter (kg-m^2)
        Pound foot square (lb-ft^2)
        Pound force inch second square (lbf-in-s^2)
        Pound inch square (lb-in^2)
        """

        ureg.define("kgm2 = kilogram * (meter ** 2)")
        ureg.define("lbft2 = 6584392202157/156250000000000 * kgm2")
        ureg.define("lbfins2 = 1129848290276167/10000000000000000 * kgm2")
        ureg.define("lbin2 = 731599133573/2500000000000000 * kgm2")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class MassPerArea:
        """
        Allows Mass Per Area unit conversions:
        Gram per square centimeter (g/cm^2)
        Gram per square foot (g/ft^2)
        Gram per square inch (g/in^2)
        Gram per square meter (g/m^2)
        Kilogram per square foot (kg/ft^2)
        Kilogram per square meter (kg/m^2)
        """

        ureg.define("g_m2 = gram / (meter ** 2)")
        ureg.define("g_cm2 = 10000 * g_m2")
        ureg.define("g_ft2 = 1562500 / 145161 * g_m2")
        ureg.define("g_in2 = 25000000 / 16129 * g_m2")
        ureg.define("kg_ft2 = 1562500000 / 145161 * g_m2")
        ureg.define("kg_m2  = 1000 * g_m2")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class MolarConcentrationGradient:
        """
        Allows Molar Concentration Gradient unit conversions:
        Mole per cubic centimeter to the power of 4 (mol/cm^4)
        Mole per cubic meter to the power of 4 (mol/m^4)
        Pound-mole per cubic foot to the power of 4 (lbmol/ft^4)
        """

        ureg.define("mol_m4 = mole / (meter ** 4)")
        ureg.define("mol_cm4 = 100000000 * mol_m4")
        ureg.define("lbmol_ft4 = 2214806494140625 / 42143431842 * mol_m4")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class MolarDensity:
        """
        Allows Molar Density unit conversions:
        Mole per cubic centimeter (mol/cm^3)
        Mole per cubic meter (mol/m^3)
        Mole per liter (mol/L)
        Pound-mole per cubic foot (lbmol/ft^3)
        """

        ureg.define("mol_m3 = mole / (meter ** 3)")
        ureg.define("mol_l = 1000 * mol_m3")
        ureg.define("lbmol_ft3 = 3543690390625/221225364 * mol_m3")
        ureg.define("mol_cm3 = 1000000 * mol_m3")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class MolarFlux:
        """
        Allows Molar Flux unit conversions:
        Kilomole per square meter per second (kmol/m^2-s)
        Mole per square meter per second (mol/m^2-s)
        """

        ureg.define("mol_m2s = 1 * (mole / ((meter ** 2) * second))")
        ureg.define("kmol_m2s = 1000 * mol_m2s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            """Converts the value to the specified unit."""
            converted_quantity = self.value * ureg(self.unit).to(to_unit)
            return converted_quantity.magnitude

    class Volume:
        ureg.define("m3 = meter ** 3")
        ureg.define("ft3 = 55306341/1953125000 * m3")
        ureg.define("gal = 473176473/125000000000 * m3")
        ureg.define("l = 1/1000 * m3")
        ureg.define("mmft3 = 442450728/15625 * m3")
        ureg.define("bbl = 9936705933/62500000000 * m3")
        ureg.define("cm3 = 1/1000000 * m3")
        ureg.define("ml = 1/1000000 * m3")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class VolumetricFlowRate:
        ureg.define("m3_s =  (meter ** 3) / second")
        ureg.define("gpm = 157725491/2500000000000 * m3_s")
        ureg.define("m3_h = 3600 * m3_s")
        ureg.define("m3_d =  86400 * m3_s")
        ureg.define("ft3_s = 55306341/1953125000 * m3_s")
        ureg.define("ft3_m= 18435447/39062500000 * m3_s")
        ureg.define("ft3_h= 6145149/781250000000 * m3_s ")
        ureg.define("ft3_d = 2048383/6250000000000 * m3_s")
        ureg.define("bbl_d = 1104078437/600000000000000 * m3_s")
        ureg.define("bbl_h = 1104078437/25000000000000 * m3_s")
        ureg.define("bbl_m = 3312235311/1250000000000 * m3_s")
        ureg.define("l_m =  1/60000 * m3_s")
        ureg.define("ml_m = 1/60000000 * m3_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class VolumetricStandardFlowrate:
        """Creates an object representing standard volumetric flowrate and allows for unit conversions.
        - MMscf/d: Million standard cubic feet per day
        - scf/d: Standard cubic feet per day
        - scf/h: Standard cubic feet per hour
        - scf/s: Standard cubic feet per second
        - sm3/d: Standard cubic meters per day
        - sm3/h: Standard cubic meters per hour
        - sm3/s: Standard cubic meters per second
        - sbbl/d: Stock tank barrels per day
        - sbbl/h: Stock tank barrels per hour
        - sbbl/min: Stock tank barrels per minute
        - Mscf/d: Thousand standard cubic feet per day
        - Msm3/d: Thousand standard cubic meters per day
        - Msm3/h: Thousand standard cubic meters per hour
        """

        ureg.define("sm3_s = (meter ** 3) / second")
        ureg.define("mmscf_d = 2048383 / 6250000 * sm3_s")
        ureg.define("scf_d = 2048383 / 6250000000000  * sm3_s")
        ureg.define("scf_h = 6145149 / 781250000000 * sm3_s")
        ureg.define("scf_s = 55306341 / 1953125000 * sm3_s")
        ureg.define("sm3_d = 1 / 86400 * sm3_s")
        ureg.define("sm3_h = 1 / 3600 * sm3_s")
        ureg.define("mscf_d = 2048383 / 6250000000 * sm3_s")
        ureg.define("msm3_d = 625 / 54 * sm3_s")
        ureg.define("msm3_h = 2500 / 9 * sm3_s")
        ureg.define("sbbl_h = 1104078437 / 25000000000000 * sm3_s")
        ureg.define("sbbl_min = 3312235311 / 1250000000000 * sm3_s")
        ureg.define("sbbl_d = 1104078437 / 600000000000000 * sm3_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class StandardVolume:
        """Creates an object representing standard volume and allows for unit conversions.
        scm3 - Standard Cubic Meter
        MMscf - Million Standard Cubic Feet
        sgal - Standard Gallon
        sL - Standard Liter
        scf - Standard Cubic Feet
        sm3 - Standard Cubic Meter
        sbbl - Standard Barrel
        Mscf - Thousand Standard Cubic Feet
        Msm3 - Thousand Standard Cubic Meters
        """

        ureg.define("sm3 = 1 * (meter ** 3)")
        ureg.define("mmscf =   442450728 / 15625  * sm3")
        ureg.define("scf = 55306341 / 1953125000 * sm3")
        ureg.define("scm3 = 1 / 1000000 * sm3")
        ureg.define("mscf = 55306341 / 1953125 * sm3")
        ureg.define("sl = 1 / 1000  * sm3")
        ureg.define("sgal = 473176473 / 125000000000 * sm3")
        ureg.define("sbbl = 9936705933 / 62500000000 * sm3")
        ureg.define("msm3 = 1000000 * sm3")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class StandardVolumetricFlowratePerLength:
        """Creates an object representing standard volumetric flowrate per length and allows for unit conversions."""

        ureg.define("m2_s = 1 * ((meter ** 2) / second)")
        ureg.define("sbbl_d_ft = 8693531 / 1440000000000 * m2_s")
        ureg.define("mm2_s = 1 / 1000000 * m2_s")
        ureg.define("cm2_s = 1 / 10000 * m2_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class Velocity:
        ureg.define("m_s = 1 * (meter / second)")
        ureg.define("m_h = 1/3600 * m_s")
        ureg.define("mph = 1397/3125 * m_s")
        ureg.define("km_h = 5/18 * m_s")
        ureg.define("km_s = 1000 * m_s")
        ureg.define("in_h = 127/18000000 * m_s")
        ureg.define("in_s = 127/5000 * m_s")
        ureg.define("ft_h = 127/1500000 * m_s")
        ureg.define("ft_s = 381/1250 * m_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class Torque:
        ureg.define("ftlb = 1 * (foot * pound)")
        ureg.define("mnm = 3389544870828501/2500000000000 * ftlb")
        ureg.define("ncm = 3389544870828501/25000000000000 * ftlb")
        ureg.define("nm = 3389544870828501/2500000000000000 * ftlb")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class Time:
        ureg.define("ms = 1/1000 * second")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class ThermalExpansion:
        ureg.define("one_c = 1/ degC")
        ureg.define("one_k = 1/ degK")
        ureg.define("one_f = 1/ degF")
        ureg.define("one_r = 1/ degR")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class ThermalConductivity:

        ureg.define("w_mc = watt / (meter * celsius)")
        ureg.define("btu_fthr = 26358756611 / 15240000000 * w_mc")
        ureg.define("cal_mhk = 523 / 450000 * w_mc")
        ureg.define("w_mk = 1 * w_mc")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class TemperatureGradient:
        ureg.define("f_ft = degF/ foot")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class TemperatureDifference:

        ureg.define("dtc = 1 * delta_degC")
        ureg.define("dtk = 1 * dtc")
        ureg.define("dtf = 5/9 * dtc")
        ureg.define("dtr = 5/9 * dtc")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            unit_map = {"c": "dtc"}
            if self.unit in unit_map:
                self.unit = unit_map[self.unit]
                converted = self.value * ureg(self.unit).to(to_unit)
                return converted.magnitude

    class Temperature:
        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            unit_map = {
                "c": "celsius",
            }
            if self.unit in unit_map:
                self.unit = unit_map[self.unit]
                temp = Q_(self.value, self.unit)
                converted = temp.to(to_unit)
                return converted.magnitude

    class SurfaceTension:
        ureg.define("n_m = N / meter")
        ureg.define("dyn_cm = 1/1000 * n_m")
        ureg.define("mn_m = 1/1000 * n_m")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class SpecificVolume:
        ureg.define("m3_kg = ((meter ** 3) / kilogram)")
        ureg.define("ft3_lb = 1769802912/28349523125 * m3_kg")
        ureg.define("in3_lb = 2048383/56699046250 * m3_kg")
        ureg.define("cm3_g = 1/1000 * m3_kg")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class SpecificMole:
        ureg.define("mol_g = mole / gram")
        ureg.define("mol_kg = 1/1000 * mol_g")
        ureg.define("lbmol_lb = 1 * mol_g")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class SpecificHeatCapacity:
        ureg.define("j_kgc = joule / (kilogram * degC)")
        ureg.define("btu_lbf = 86265021636/20617835 * j_kgc")
        ureg.define("btu_lbr = 86265021636/20617835 * j_kgc")
        ureg.define("j_kgk = 1 * j_kgc")
        ureg.define("kj_kgc = 1000 * j_kgc")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class SpecificEnthalpy:
        ureg.define("j_g = joule / gram")
        ureg.define("j_kg = 1/1000 * j_g")
        ureg.define("kj_kg = 1 * j_g")
        ureg.define("btu_lb = 2396250601/1030891750 * j_g")
        ureg.define("cal_kg = 523/125000 * j_g")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class SpecificCapacity:
        ureg.define("m3_r = (meter **3) / degR")
        ureg.define("ft3_r = 55306341/1953125000 * m3_r")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class RevolutionsPerTime:
        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class RateOfChangeOfTemperature:
        ureg.define("c_s = celsius / second")
        ureg.define("f_s = 5/9 * c_s")
        ureg.define("k_s = 1 * c_s")
        ureg.define("r_s = 5/9 * c_s")
        ureg.define("c_m = 1/60 * c_s")
        ureg.define("f_m = 1/108 * c_s")
        ureg.define("c_h = 1/3600 * c_s")
        ureg.define("f_h = 1/6480 * c_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class RateOfChangeOfPressure:
        ureg.define("pa_s = Pa / second")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class RateOfChangeOfDensity:
        ureg.define("kg_m3s = kilogram / (meter ** 3) * second")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class PressureGradient:
        ureg.define("pa_m = Pa / meter")
        ureg.define("psi_ft = 8896443230521/393289536 * pa_m")
        ureg.define("kpa_m = 1000 * pa_m")
        ureg.define("bar_m = 1 * 100000 * pa_m")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class PressureDifference:
        ureg.define("pa = 1 * Pa")
        ureg.define("kpa = 1000 * pa")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class Pressure:
        ureg.define("pa = 1 * Pa")
        ureg.define("kpa = 1000 * pa")
        ureg.define("barg = 100000 * pa")
        ureg.define("bara = 100000 * pa")
        ureg.define("bar = 100000 * pa")
        ureg.define("atm = 101325 * pa ")
        ureg.define("mpa = 1000000 * pa")
        ureg.define("psi = 8896443230521 / 1290320000 * pa")
        ureg.define("psia = 8896443230521 / 1290320000 * pa")
        ureg.define("psig = 8896443230521 / 1290320000 * pa")
        ureg.define("kgf_cm2 = 196133 / 2 * pa")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            if to_unit == "psig":
                convert = self.value * ureg(self.unit).to(ureg.psia)
                converted = convert.magnitude - 14.7
                return converted
            elif to_unit == "barg":
                convert = self.value * ureg(self.unit).to(ureg.bara)
                converted = convert.magnitude - 1.01
                return converted
            else:
                converted = self.value * ureg(self.unit).to(to_unit)
                return converted.magnitude

    class Power:
        ureg.define("w = 1 * watt")
        ureg.define("btu_h = 26358756611/90000000000 * w")
        ureg.define("hp = 37284993579113511/50000000000000 * w")
        ureg.define("kw = 1000 * w")
        ureg.define("mw = 1/1000 * w")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class OneOverLength:
        ureg.define("one_m = 1 / meter")
        ureg.define("one_cm = 100 * one_m")
        ureg.define("one_ft = 1250/381 * one_m")
        ureg.define("one_km = 1/1000 * one_m")
        ureg.define("one_mi = 125/201168 * one_m")
        ureg.define("one_mm = 1000 * one_m")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class OneOverFlowrate:
        ureg.define("d_m3 = d / (meter ** 3)")
        ureg.define("d_bbl = 62500000000/9936705933 * d_m3")
        ureg.define("min_bbl = 390625000/89430353397 * d_m3")
        ureg.define("d_ft3 = 1953125000/55306341 * d_m3")
        ureg.define("h_ft3 = 244140625/165919023 * d_m3")
        ureg.define("s_ft3 = 9765625/23892339312 * d_m3")
        ureg.define("h_m3 = 1/24* d_m3")
        ureg.define("s_m3 = 1/86400 * d_m3")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class Moles:
        ureg.define("mol = 1 * mole")
        ureg.define("kmol = 1000 * mol")
        ureg.define("lbmol = 45359237/100000 * mol")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class MoleDensityPerTemperature:
        ureg.define("mol_m3k = mole / ((meter ** 3) * degK)")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class MolecularWeight:
        ureg.define("g_mol = gram / mole")
        ureg.define("kg_kmol = 1 * g_mol")
        ureg.define("kg_mol = 1000 * g_mol")
        ureg.define("lb_lbmol = 1 * g_mol")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class MolarVolume:
        ureg.define("m3_mol = ((meter ** 3) / mole)")
        ureg.define("cm3_mol = 1/1000000 * m3_mol")
        ureg.define("l_mol = 1/1000 * m3_mol")
        ureg.define("ft3_lbmol = 221225364/3543690390625 * m3_mol")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude

    class MolarRate:
        ureg.define("mol_s = mole / second")
        ureg.define("kmol_s = 1000 * mol_s")
        ureg.define("lbmol_s = 45359237/100000 * mol_s")

        def __init__(self, value, unit):
            self.value = value
            self.unit = unit

        def convert(self, to_unit):
            converted = self.value * ureg(self.unit).to(to_unit)
            return converted.magnitude
