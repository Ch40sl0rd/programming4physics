import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as si

def air_density(z):
    '''
        This function describes the decrease in air density when going to bigger heights.

        input:
        - z : np.array or scalar of height z in meters

        return:
        - np.array or scalar of air density at height z in kg/m^3
    '''
    return 1.22*np.exp(-z/10000)

def parachute(t):
    '''
        This function describes the opening of the parachute and the resulting
        increase in area.

        input:
        - t : np.array or scalar for time t in seconds

        return:
        - np.array or scalar, area of the parachute at time t in m^2
    '''
    return 1 + 50*(1 - np.exp(-t/5))/(1 + np.exp(-t/5))

def phase1(S, t):
    '''
        This function implements the first phase of baumgartners jump from 39 km to 2 km above ground.
        Here there is no parachute open and the jump is modelled as a free fall with air friction.

        inputs:
        - S : tuple with two elements, z-coordinates and velocity v (z,v)
        - t : np.array of time

        return:
        - tuple with two elements, derivates of z-coordinates and velocity v (z',v')
    '''
    z, v = S
    return (-v,
            9.8 - 0.5*air_density(z)*0.3*0.9/118*v**2)

def phase2(S, t):
    '''
        This function implements phase 2 of baumgartners jump from 2 km to landing.
        Here the parachute is opened and the descend rate rapidly decreases.

        inputs:
        - S : tuple with two elements, z-coordinates and velocity v (z,v)
        - t : np.array of time

        return:
        - tuple with two elements, derivates of z-coordinates and velocity v (z',v')
    '''
    z, v = S
    return (-v,
            9.8 - 0.5*1.22*1.5/118*parachute(t)*v**2)   

#starting conditions for phase 1 of the jump
phase1_S0 = (39000, 0)
#create time ofsufficient length
t = np.linspace(0, 1000, 10000)
#solve DE for phase 1 of the jump
sol1 = si.odeint(phase1, y0=phase1_S0, t=t)

#extract time, z-coordinate and velocity from solution
#phase 1 ends at height of about 2 km
t1 = t[sol1[:,0]>2000]
z1 = sol1[:,0][sol1[:,0]>2000]
v1 = sol1[:,1][sol1[:,0]>2000]

#get starting conditions for phase 2 from end of phase 1
phase2_S0 = (z1[-1], v1[-1])
#solve DE for phase 2 of the jump
sol2 = si.odeint(phase2, y0=phase2_S0, t=t)
#extract time, z-coordinate and velocity from solution
#phase 2 ends at height of 0 m
t2 = t[sol2[:,0]>0] + t1[-1] #shift time by duration of phase 1
z2 = sol2[:,0][sol2[:,0]>0]
v2 = sol2[:,1][sol2[:,0]>0]

#plot results for z-ccorindates and velocity in one figure
fig, axes = plt.subplots(1, 2, figsize=(10,5))
fig.suptitle('Baumgartners parachute jump')
axes[0].plot(t1, z1, label='phase 1: free fall')
axes[0].plot(t2, z2, label='phase 2: parachute open')
axes[0].set_xlabel('time t / s')
axes[0].set_ylabel('height z / m')
axes[0].set_title('Height')
axes[0].legend()
axes[1].plot(t1, v1, label='phase 1: free fall')
axes[1].plot(t2, v2, label='phase 2: parachute open')
axes[1].set_xlabel('time t / s')
axes[1].set_ylabel('velocity v / m/s')
axes[1].set_title('Velocity')
axes[1].legend()
plt.show()

#print out results of questions asked
print(f'The maxmimum absolute velocity during the jump was {np.max(v1):.1f} m/s')
print(f'The final speed at the surface is {v2[-1]:.1f} m/s')
print(f'The complete jump took around {t2[-1]:.1f} s')