import pytest
import uuid

from app.models.calculation import (
    Calculation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Exponentiation,
    NthRoot,
    Modulus,
)

# Helper function to create a dummy user_id for testing.
def dummy_user_id():
    return uuid.uuid4()

def test_addition_get_result():
    """
    Test that Addition.get_result returns the correct sum.
    """
    inputs = [10, 5, 3.5]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    result = addition.get_result()
    assert result == sum(inputs), f"Expected {sum(inputs)}, got {result}"

def test_subtraction_get_result():
    """
    Test that Subtraction.get_result returns the correct difference.
    """
    inputs = [20, 5, 3]
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=inputs)
    # Expected: 20 - 5 - 3 = 12
    result = subtraction.get_result()
    assert result == 12, f"Expected 12, got {result}"

def test_multiplication_get_result():
    """
    Test that Multiplication.get_result returns the correct product.
    """
    inputs = [2, 3, 4]
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=inputs)
    result = multiplication.get_result()
    assert result == 24, f"Expected 24, got {result}"

def test_division_get_result():
    """
    Test that Division.get_result returns the correct quotient.
    """
    inputs = [100, 2, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    # Expected: 100 / 2 / 5 = 10
    result = division.get_result()
    assert result == 10, f"Expected 10, got {result}"

def test_division_by_zero():
    """
    Test that Division.get_result raises ValueError when dividing by zero.
    """
    inputs = [50, 0, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()

def test_exponentiation_get_result():
    inputs = [4, 3, 2]  # Left-to-right: (4^3)^2 = 4096
    exp_calc = Exponentiation(user_id=dummy_user_id(), inputs=inputs)
    result = exp_calc.get_result()
    assert result == 4096, f"Expected 4096, got {result}"

def test_nthroot_get_result():
    inputs = [4096, 2, 3]  # Sequential roots: ((4096^(1/2))^(1/3)) ≈ 4
    root_calc = NthRoot(user_id=dummy_user_id(), inputs=inputs)
    result = root_calc.get_result()
    assert abs(result - 4) < 1e-9, f"Expected 4, got {result}"

def test_modulus_get_result():
    inputs = [27, 6, 4]  # 27 % 6 % 4 = 3
    mod_calc = Modulus(user_id=dummy_user_id(), inputs=inputs)
    result = mod_calc.get_result()
    assert result == 3, f"Expected 3, got {result}"

def test_calculation_factory_addition():
    """
    Test the Calculation.create factory method for addition.
    """
    inputs = [1, 2, 3]
    calc = Calculation.create(
        calculation_type='addition',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Check that the returned instance is an Addition.
    assert isinstance(calc, Addition), "Factory did not return an Addition instance."
    assert calc.get_result() == sum(inputs), "Incorrect addition result."

def test_calculation_factory_subtraction():
    """
    Test the Calculation.create factory method for subtraction.
    """
    inputs = [10, 4]
    calc = Calculation.create(
        calculation_type='subtraction',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 10 - 4 = 6
    assert isinstance(calc, Subtraction), "Factory did not return a Subtraction instance."
    assert calc.get_result() == 6, "Incorrect subtraction result."

def test_calculation_factory_multiplication():
    """
    Test the Calculation.create factory method for multiplication.
    """
    inputs = [3, 4, 2]
    calc = Calculation.create(
        calculation_type='multiplication',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 3 * 4 * 2 = 24
    assert isinstance(calc, Multiplication), "Factory did not return a Multiplication instance."
    assert calc.get_result() == 24, "Incorrect multiplication result."

def test_calculation_factory_division():
    """
    Test the Calculation.create factory method for division.
    """
    inputs = [100, 2, 5]
    calc = Calculation.create(
        calculation_type='division',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 100 / 2 / 5 = 10
    assert isinstance(calc, Division), "Factory did not return a Division instance."
    assert calc.get_result() == 10, "Incorrect division result."

def test_calculation_factory_exponentiation():
    inputs = [2, 3, 2]  # (2^3)^2 = 64
    calc = Calculation.create(
        calculation_type='exponentiation',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    assert isinstance(calc, Exponentiation)
    assert calc.get_result() == 64

def test_calculation_factory_nthroot():
    inputs = [64, 2, 3]  # ((64^(1/2))^(1/3)) ≈ 2
    calc = Calculation.create(
        calculation_type='nthroot',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    assert isinstance(calc, NthRoot)
    assert abs(calc.get_result() - 2) < 1e-7

def test_calculation_factory_modulus():
    inputs = [20, 7, 3]  # 20 % 7 % 3 = 6 % 3 = 0
    calc = Calculation.create(
        calculation_type='modulus',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    assert isinstance(calc, Modulus)
    assert calc.get_result() == 0

def test_calculation_factory_invalid_type():
    """
    Test that Calculation.create raises a ValueError for an unsupported calculation type.
    """
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        Calculation.create(
            calculation_type='absolutevalue',  # unsupported type
            user_id=dummy_user_id(),
            inputs=[10, 3],
        )

def test_invalid_inputs_for_addition():
    """
    Test that providing non-list inputs to Addition.get_result raises a ValueError.
    """
    addition = Addition(user_id=dummy_user_id(), inputs="not-a-list")
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        addition.get_result()

def test_invalid_inputs_for_subtraction():
    """
    Test that providing fewer than two numbers to Subtraction.get_result raises a ValueError.
    """
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=[10])
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        subtraction.get_result()

def test_invalid_inputs_for_division():
    """
    Test that providing fewer than two numbers to Division.get_result raises a ValueError.
    """
    division = Division(user_id=dummy_user_id(), inputs=[10])
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        division.get_result()

def test_invalid_inputs_for_exponentiation():
    """
    Test that providing non-list inputs or fewer than two numbers
    to Exponentiation.get_result raises a ValueError.
    """
    # Non-list input
    exp_calc = Exponentiation(user_id=dummy_user_id(), inputs="not-a-list")
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        exp_calc.get_result()

    # Less than two numbers
    exp_calc = Exponentiation(user_id=dummy_user_id(), inputs=[2])
    with pytest.raises(ValueError, match="Exponentiation requires at least two inputs."):
        exp_calc.get_result()

def test_invalid_inputs_for_nthroot():
    """
    Test that providing non-list inputs, fewer than two numbers,
    zero roots, or even root of negative numbers raises a ValueError.
    """
    # Non-list input
    root_calc = NthRoot(user_id=dummy_user_id(), inputs="not-a-list")
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        root_calc.get_result()

    # Less than two numbers
    root_calc = NthRoot(user_id=dummy_user_id(), inputs=[16])
    with pytest.raises(ValueError, match="NthRoot requires at least two inputs."):
        root_calc.get_result()

    # Zero as root
    root_calc = NthRoot(user_id=dummy_user_id(), inputs=[16, 0])
    with pytest.raises(ValueError, match="Cannot take root with degree zero."):
        root_calc.get_result()

    # Even root of negative number
    root_calc = NthRoot(user_id=dummy_user_id(), inputs=[-16, 2])
    with pytest.raises(ValueError, match="Cannot take even root of negative number."):
        root_calc.get_result()

def test_invalid_inputs_for_modulus():
    """
    Test that providing non-list inputs, fewer than two numbers,
    or zero as a divisor raises a ValueError for Modulus.
    """
    # Non-list input
    mod_calc = Modulus(user_id=dummy_user_id(), inputs="not-a-list")
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        mod_calc.get_result()

    # Less than two numbers
    mod_calc = Modulus(user_id=dummy_user_id(), inputs=[10])
    with pytest.raises(ValueError, match="Modulus requires at least two inputs."):
        mod_calc.get_result()

    # Zero as divisor
    mod_calc = Modulus(user_id=dummy_user_id(), inputs=[10, 0])
    with pytest.raises(ValueError, match="Cannot take modulus with zero."):
        mod_calc.get_result()

