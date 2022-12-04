massless_track_geo_energy = 432.425
mass = 588
drag_coefficient = 0.1
frontal_area = 1.864
motor_efficiency = 0.98
auxiliary_power = 30.0
wheel_radius = 0.2715
init_v = 40
track_length = 4197

def lap_energy(v, total_mass, solar_input, air_density): # Energy used in a lap given the conditions and velocity
    return track_length*(auxiliary_power - solar_input)/v \
        + (track_length * drag_coefficient * air_density * frontal_area * v**2/2 + total_mass*massless_track_geo_energy)/motor_efficiency

def del_lap_energy(v, solar_input, air_density): # Energy used in lap, velocity differential
    return -track_length*(auxiliary_power - solar_input)/(v**2) \
        + (track_length * drag_coefficient * air_density * frontal_area * v)/motor_efficiency

def lamb(lap_number = 0, current_battery = 136800000, occupant_mass = 80, solar_input = 570, air_density = 1.225): # Lambda function. Produces recommended RPM.

    distance_remaining = 1000000-track_length*lap_number
    lap_battery_allocation = current_battery*track_length/distance_remaining

    total_mass = mass+occupant_mass

    v = init_v

    diff = lap_energy(v, total_mass, solar_input, air_density) - lap_battery_allocation

    while (abs(diff)>1000) :

        v -= diff/del_lap_energy(v, solar_input, air_density) # Newton iteration: x_{n+1} = x_n - f(x_n)/f'(x_n)

        diff = lap_energy(v, total_mass, solar_input, air_density) - lap_battery_allocation

        if (v<0 or diff<0):
            raise Exception("Newton iteration failed! Check that inputs are sensible.")

    rpm = 60*v/(wheel_radius*2*3.1415)

    return rpm

