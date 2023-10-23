def convert_temp(unit_in, unit_out, temp):
    """Convert farenheit <-> celsius and return results.

    - unit_in: either "f" or "c" 
    - unit_out: either "f" or "c"
    - temp: temperature (in f or c, depending on unit_in)

    Return results of conversion, if any.

    If unit_in or unit_out are invalid, return "Invalid unit [UNIT_IN]".

    For example:

      convert_temp("c", "f", 0)  =>  32.0
      convert_temp("f", "c", 212) => 100.0
    """

    # YOUR CODE HERE
def convert_temp(from_unit, to_unit, temp):
    valid_units = {"c", "f"}
    
    if from_unit not in valid_units:
        return f"Invalid unit {from_unit}"
    if to_unit not in valid_units:
        return f"Invalid unit {to_unit}"
    
    if from_unit == "c" and to_unit == "f":
        return (temp * 9/5) + 32
    if from_unit == "f" and to_unit == "c":
        return (temp - 32) * 5/9
    
print("c", "f", 0, convert_temp("c", "f", 0), "should be 32.0")
print("f", "c", 212, convert_temp("f", "c", 212), "should be 100.0")
print("z", "f", 32, convert_temp("z", "f", 32), "should be Invalid unit z")
print("c", "z", 32, convert_temp("c", "z", 32), "should be Invalid unit z")
print("f", "f", 75.5, convert_temp("f", "f", 75.5), "should be 75.5")
print("test")
